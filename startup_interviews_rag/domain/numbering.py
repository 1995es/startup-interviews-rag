"""Turn and sentence numbering for the segmentation LLM (step 1 of
docs/llm-ingestion.md).

    [t020 00:07:15 SPEAKER_01] Yes, yes, of course. As I said, it is fragmented...

Turns longer than `max_words` are split into sentences with IDs `t021.s1`,
`t021.s2`... so the LLM can cut inside a monologue:

    [t021 00:07:40 SPEAKER_01]
    [t021.s1] First sentence.
    [t021.s2] Second sentence.
"""

import re
from dataclasses import asdict, dataclass, fields
from typing import Self

from startup_interviews_rag.domain.timecode import hhmmss
from startup_interviews_rag.domain.transcript import DEFAULT_SPEAKER, Turn
from startup_interviews_rag.domain.video import VideoMeta

# Sentence end: `.`, `?` or `!` (plus closing quotes or brackets) followed by
# whitespace. Splitting "S.A." or "3.5" is harmless: just one extra candidate cut.
SENT_SPLIT = re.compile(r"(?<=[.?!])(?:[\"'»)\]]*)\s+")

# Turns longer than this are split into sentences.
DEFAULT_MAX_TURN_WORDS = 150


@dataclass(frozen=True)
class IdUnit:
    """A cuttable ID with its original text, speaker and turn timings: what
    validation (step 3), chunk cutting (step 4) and timestamps (step 5) work
    from."""

    id: str
    turn: str
    speaker: str
    start: float | None
    end: float | None
    text: str

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(**{f.name: data.get(f.name) for f in fields(cls)})

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class LLMInput:
    """llm_input/<id>.txt (`prompt`) plus llm_input/<id>.json (the rest)."""

    video_id: str
    meta: VideoMeta
    prompt: str
    units: list[IdUnit]

    @property
    def speaker_labels(self) -> list[str]:
        return sorted({u.speaker for u in self.units})

    @property
    def split_turns(self) -> int:
        """How many turns were split into sentences."""
        return len({u.turn for u in self.units if u.id != u.turn})


def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in SENT_SPLIT.split(text) if s.strip()]


def number_turns(turns: list[Turn], max_words: int) -> tuple[list[str], list[IdUnit]]:
    """Returns the numbered lines for the prompt and the list of cuttable
    units. A turn split into sentences is not cuttable itself: only its
    sentences are."""
    width = max(3, len(str(len(turns))))
    lines: list[str] = []
    units: list[IdUnit] = []

    for i, turn in enumerate(turns, start=1):
        tid = f"t{i:0{width}d}"
        text = (turn.text or "").strip()
        speaker = turn.speaker or DEFAULT_SPEAKER
        head = f"{tid} {hhmmss(turn.start)} {speaker}"

        sentences = split_sentences(text) if len(text.split()) > max_words else []
        if len(sentences) < 2:
            lines.append(f"[{head}] {text}")
            units.append(IdUnit(tid, tid, speaker, turn.start, turn.end, text))
            continue

        lines.append(f"[{head}]")
        for k, sentence in enumerate(sentences, start=1):
            sid = f"{tid}.s{k}"
            lines.append(f"[{sid}] {sentence}")
            units.append(IdUnit(sid, tid, speaker, turn.start, turn.end, sentence))

    return lines, units


def render_header(meta: VideoMeta) -> str:
    description = (meta.description or "").strip() or "(no description)"
    return "\n".join(
        [
            "# Episode",
            "",
            f"Title: {meta.title or ''}",
            f"Date: {meta.published or 'unknown'}",
            f"URL: {meta.webpage_url or ''}",
            "",
            "Description:",
            description,
        ]
    )


def build_llm_input(meta: VideoMeta, turns: list[Turn], max_words: int) -> LLMInput:
    lines, units = number_turns(turns, max_words)
    prompt = render_header(meta) + "\n\n# Transcript\n\n" + "\n".join(lines) + "\n"
    return LLMInput(video_id=meta.id, meta=meta, prompt=prompt, units=units)
