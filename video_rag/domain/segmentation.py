"""Episode segmentation by an LLM (step 2 of docs/ingesta-llm.md): the
prompt, the response schema and the retry feedback. Provider-neutral: the
LLM call itself goes through the `LLMProvider` port.

The LLM returns only IDs and metadata, never transcript text:

    speakers         SPEAKER_XX -> {name, role, company}
    units            contiguous {from, to} ranges + type, title, summary,
                     raw_tags (free, generic business topics) and questions
    glossary         fixes for mistranscribed names
    episode_summary  3-5 sentences

There is no closed taxonomy: raw_tags are free text. Mapping them to
canonical tags is a later, separate step (step 9) that does not require
segmenting again.
"""

import json

# Bumping it invalidates every cached segments/<id>.json.
PROMPT_VERSION = "seg-2"

# These are data, not code: they end up in the Qdrant payload, in Spanish.
UNIT_TYPES = ["anecdota", "consejo", "opinion", "dato", "relleno"]
ROLES = ["anfitrión", "invitado", "otro"]

SYSTEM_PROMPT = """\
You are the segmenter of a retrieval (RAG) system over Itnig's podcasts and \
interviews about entrepreneurship, all in Spanish. You receive the full, \
numbered transcript of one episode and return where to cut it into thematic \
units, plus metadata for each unit. Each unit is indexed on its own, so what \
matters is that a retrieved fragment makes sense without the rest of the \
episode.

## Input format

Every speaking turn carries an ID, its start time and the speaker label from \
automatic diarization:

    [t020 00:07:15 SPEAKER_01] Sí, sí, claro. Como digo, está fragmentado...

Long turns come split into sentences. In that case the turn line has no text \
and the valid IDs are those of its sentences (t021.s1, t021.s2...), not the \
turn's own ID (t021):

    [t021 00:07:40 SPEAKER_01]
    [t021.s1] Primera frase.
    [t021.s2] Segunda frase.

The transcript is automatic: proper names are often misspelled, and \
diarization sometimes attributes an interviewer's question to the guest's \
turn. Sentence-level IDs exist precisely so those cases can be separated.

## What to return

**speakers**: one entry per SPEAKER_XX label that appears in the transcript, \
with name, role and company. Infer them from the introductions, the title and \
the video description. If a field cannot be known, use null rather than \
guessing.

**units**: {from, to} ID ranges that cover the whole episode, in order, with \
no gaps and no overlaps: the first unit starts at the first ID, each unit \
starts at the ID right after the previous unit's `to`, and the last one ends \
at the last ID. `from` and `to` may be the same ID. Each unit tells one thing \
(an anecdote, a piece of advice, an explanation) and stands on its own. Cut \
where the topic changes, not where the speaker changes: a question goes in \
the same unit as its answer.

Size: between 80 and 600 words per unit, roughly 30 seconds to 3.5 minutes \
of conversation (use the turn timestamps as a guide). A shorter unit carries \
too little context for retrieval; a longer one mixes topics and its embedding \
resembles none of them. If a topic runs longer, split it along its subtopics.

For each unit:
- type: anecdota (something that happened), consejo (actionable advice), \
opinion (a judgement or stance), dato (figures, facts, explanations of how \
something works) or relleno (greetings, courtesy introductions, jokes, ads, \
goodbyes, small talk without content). Filler is not indexed and is exempt \
from the size limit, so group it into units of its own instead of attaching \
it to a unit with content.
- title: short, concrete headline.
- summary: 1-2 sentences naming the people and companies involved, written \
so it can be understood without having seen the episode.
- raw_tags: 0 to 4 tags naming the business or entrepreneurship problem the \
unit is about, the way a founder would browse a library of experiences: \
"primeros clientes", "pivote", "financiación", "contratación", "pricing", \
"internacionalización", "cofundadores". Rules:
  - Generic and reusable across any company and sector. Never a sector, \
product, company, person or place from this episode: for a unit about how \
Nautal got its first boats, "primeros clientes" is right and "barcos", \
"alquiler de barcos" or "Nautal" are wrong; for Wallbox, "vehículo \
eléctrico" is wrong. A technology is acceptable only when it is the topic \
itself and cuts across companies (for example "inteligencia artificial").
  - In Spanish, lowercase, 1 to 3 words, no hyphens.
  - Prefer the plainest, most common name over jargon or anglicisms: \
"primeros clientes", not "early adopters", "tracción inicial" or \
"go-to-market".
  - Filler units get no tags. No tag is better than a forced one.
- questions: 2 to 4 questions the unit answers, phrased the way a user would \
type them into a search box, without assuming they know the episode.

**glossary**: mistranscribed proper names and their correct form (for \
example "Autal" -> "Nautal", "Citrocket" -> "Seedrocket"). Only fixes you can \
justify from the title, the description or the context; use the correct form \
in titles, summaries and questions.

**episode_summary**: 3-5 sentences: who takes part, from which company, and \
what they talk about.

Write title, summary, questions and episode_summary in Spanish from Spain: \
it is the language of the transcript and of the people who will search it, \
and the questions are matched against their queries. Do not copy \
transcript text into the output beyond what is essential: cuts are made by \
ID only.
"""


def nullable(schema: dict) -> dict:
    return {"anyOf": [schema, {"type": "null"}]}


def output_schema(labels: list[str]) -> dict:
    """JSON schema of the response. Unit types and speaker labels are enums
    so the model cannot step outside them; raw_tags are free by design; IDs
    are not enums either (they would be thousands of values) and are checked
    in step 3."""
    speaker = {
        "type": "object",
        "properties": {
            "label": {"type": "string", "enum": labels},
            "name": nullable({"type": "string"}),
            "role": {"type": "string", "enum": ROLES},
            "company": nullable({"type": "string"}),
        },
        "required": ["label", "name", "role", "company"],
        "additionalProperties": False,
    }
    unit = {
        "type": "object",
        "properties": {
            "from": {"type": "string"},
            "to": {"type": "string"},
            "type": {"type": "string", "enum": UNIT_TYPES},
            "title": {"type": "string"},
            "summary": {"type": "string"},
            "raw_tags": {"type": "array", "items": {"type": "string"}},
            "questions": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["from", "to", "type", "title", "summary", "raw_tags", "questions"],
        "additionalProperties": False,
    }
    glossary = {
        "type": "object",
        "properties": {"wrong": {"type": "string"}, "right": {"type": "string"}},
        "required": ["wrong", "right"],
        "additionalProperties": False,
    }
    return {
        "type": "object",
        "properties": {
            "speakers": {"type": "array", "items": speaker},
            "units": {"type": "array", "items": unit},
            "glossary": {"type": "array", "items": glossary},
            "episode_summary": {"type": "string"},
        },
        "required": ["speakers", "units", "glossary", "episode_summary"],
        "additionalProperties": False,
    }


def retry_feedback(errors: list[str], previous: dict | None) -> str:
    """Tail appended after the transcript on the single validation retry
    (step 3), so the transcript prefix stays cacheable."""
    lines = ["Your previous response failed validation for these reasons:", ""]
    lines += [f"- {e}" for e in errors]
    if previous is not None:
        lines += ["", "Previous response:", json.dumps(previous, ensure_ascii=False)]
    lines += ["", "Return the full, corrected segmentation."]
    return "\n".join(lines)
