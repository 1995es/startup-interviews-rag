# video-rag

A retrieval-augmented generation (RAG) system over the interviews of
[Itnig](https://www.youtube.com/@itnig), a Spanish podcast about startups and
entrepreneurship. Ask *"how do I find my first customers?"* or *"how do I validate an
idea?"* and get back what the founders who were interviewed actually did, with a link
to the exact minute of the video where they tell it.

> **Status: work in progress.** The ingestion pipeline (video → transcript → LLM
> segmentation) works; chunking, embeddings, the vector store and the query frontend
> are next. See [Roadmap](#roadmap).

## How it works

```
YouTube URL
  → audio (yt-dlp, 16 kHz mono wav)
  → transcript with word timings (WhisperX: Whisper large-v2 + forced alignment)
  → who speaks when (pyannote diarization)
  → speaker turns, cut per word                         output/<id>.json
  → numbered turns and sentences for the LLM            llm_input/<id>.txt     ✅ done
  → one LLM call per episode: thematic units, speakers,
    summaries, tags, questions each unit answers        segments/<id>.json     ✅ done
  → validate, build chunks, contextual headers                                 🚧 next
  → embeddings (BGE-M3: dense + sparse + multi-vector)                         ⏳ planned
  → Qdrant                                                                     ⏳ planned
  → API + web frontend for questions                                           ⏳ planned
```

The core idea: an LLM reads each full episode **once** and returns *where to cut it*
(only turn and sentence IDs, never text), who each speaker is and metadata for each
unit: type (anecdote, advice, opinion, fact, filler), a summary, free topic tags such as
*first customers* or *fundraising*, and the questions the unit answers. Chunks are
always cut from the original transcript, so the LLM cannot alter what the interviewee
said. The full design is in [`docs/llm-ingestion.md`](docs/llm-ingestion.md).

## Roadmap

| Phase | What | Status |
|---|---|---|
| Transcription | WhisperX + word alignment + diarization, speaker turns cut per word | ✅ Done |
| Corpus sample | 10 random Itnig episodes transcribed (10.2 h, 104k words) in [`transcripts/`](transcripts/) | ✅ Done |
| Ingestion, step 1 | Numbered LLM input with turn and sentence IDs | ✅ Done |
| Ingestion, step 2 | LLM segmentation with a JSON schema, cached on disk, two providers | ✅ Done |
| Diarization quality | Check whether pyannote's exclusive diarization fixes misattributed interjections ([notebook](notebooks/h1_diarization_check.ipynb)) | 🚧 In progress |
| Ingestion, steps 3–6 | Validation with retry, chunk building, timestamps, contextual headers | ⏳ Planned |
| Indexing | BGE-M3 embeddings into Qdrant (`docker-compose.yml` is ready) | ⏳ Planned |
| Querying | Retrieval + answer generation, evaluation on a golden set | ⏳ Planned |
| Interface | API and web frontend | ⏳ Planned |

## Architecture

The code is a Python package, [`video_rag/`](video_rag/), with a hexagonal (ports and
adapters) architecture, so the API and the frontend can be added later without touching
the pipeline logic:

```
video_rag/
├── domain/          pure logic: turn building, numbering, segmentation prompt and schema
├── application/
│   ├── ports/       abstract classes the use cases depend on
│   └── use_cases/   PrepareLLMInput, SegmentEpisode, RenderScript
├── infrastructure/  adapters: WhisperX, yt-dlp, Anthropic, OpenRouter, JSON files
├── interfaces/cli/  the command-line scripts (an api/ will sit next to it)
├── config.py        settings from the environment and .env
└── container.py     composition root: the only module that picks adapters
```

`domain` and `application` never import third-party SDKs or infrastructure;
dependencies are injected by hand through constructors. That is what lets the test
suite run without network or models, using in-memory fakes of the ports.

The LLM sits behind an `LLMProvider` port with two adapters, `AnthropicProvider`
(default, `claude-opus-5-5`) and `OpenRouterProvider`. Switching provider is a matter of
configuration, not code.

## Getting started

Requirements: Python 3.11–3.12, [Poetry](https://python-poetry.org/) 2.x and `ffmpeg`
on the PATH (`brew install ffmpeg` / `apt install ffmpeg` / `winget install Gyan.FFmpeg`).
An NVIDIA GPU is recommended; without one the pipeline falls back to CPU/int8, which is
much slower.

```bash
poetry install
cp .env.template .env   # fill in the keys you need
```

`.env` holds:

```bash
HF_TOKEN=hf_...                  # optional: speaker diarization
LLM_PROVIDER=anthropic           # anthropic (default) | openrouter
LLM_MODEL=                       # optional: defaults to the provider's model
ANTHROPIC_API_KEY=sk-ant-...     # only the chosen provider's key is required
OPENROUTER_API_KEY=sk-or-...
```

Diarization needs a [Hugging Face](https://huggingface.co/) token and the terms of
[`pyannote/speaker-diarization-3.1`](https://huggingface.co/pyannote/speaker-diarization-3.1)
accepted with the same account. Without it, the audio is still transcribed but every
turn comes out as `SPEAKER_00`.

No GPU? The [Colab notebook](notebooks/h1_diarization_check.ipynb) runs the
transcription and diarization part on a free T4.

## Usage

The scripts live in [`video_rag/interfaces/cli/`](video_rag/interfaces/cli/) and run
by path:

```bash
# Step 1: URL -> metadata, transcript and numbered LLM input
poetry run python video_rag/interfaces/cli/prepare.py "https://www.youtube.com/watch?v=yOLw6ncCJwY" --language es --min-speakers 2

# Step 2: LLM segmentation of one episode (or of every prepared one, without an id)
poetry run python video_rag/interfaces/cli/segment.py yOLw6ncCJwY [--provider openrouter] [--model ...] [--force]

# Transcript -> readable Markdown script
poetry run python video_rag/interfaces/cli/script.py output/yOLw6ncCJwY.json --timestamps
```

`prepare.py` writes `meta/<id>.json` (title, date, description), `audio/<id>.wav`,
`output/<id>.json` and `llm_input/<id>.txt`. Stored metadata and transcripts are reused
without network or WhisperX; `--force` redoes them (the wav is always reused). Options:
`--model` (`tiny`…`large-v3`, default `large-v2`), `--language`, `--min-speakers` /
`--max-speakers` and `--min-words`.

The transcript is a flat list of speaker turns:

```json
[
  {"text": "para ver si me abren.", "speaker": "SPEAKER_02", "start": 3.284, "end": 4.045}
]
```

`segment.py` caches its result in `segments/<id>.json`, keyed by model and prompt
version, so a rerun does not call the LLM again.

`script.py` turns a transcript into Markdown, one line per turn
(`--names SPEAKER_00=Jordi,SPEAKER_01=Bernat` for real names, `--table` for a table).

## Development

```bash
poetry run pytest                 # no network, no models
poetry run ruff format .
poetry run ruff check . --fix
```

## Design notes

**Speaker turns are cut per word, not per segment.** A Whisper segment lasts about
20 s and often holds both a question and its answer, so grouping by segment speaker
destroys the dialogue (643 fake turns vs. 547 real ones in the sample video).
[`domain/turns.py`](video_rag/domain/turns.py) rebuilds turns from each word's speaker
and applies two fixes: `smooth_runs` absorbs runs shorter than `--min-words` (diarization
flips speaker on isolated words) and `snap_to_sentences` moves each boundary to the
nearest sentence end within ±3 words.

**Long turns are split into sentences for the LLM.** Only 10 % of the turns are longer
than 150 words, but they hold 46 % of the words: that is where guests tell their
stories. Giving each sentence its own ID lets the LLM cut a multi-topic monologue into
separate units.

**The LLM never writes the text that gets indexed.** It returns ID ranges and
metadata; chunks are cut from the original transcript. The response follows a strict
JSON schema and is cached by model and prompt version.

**Graceful degradation.** If the model fails to load on the GPU it retries on CPU/int8;
without `HF_TOKEN` it skips diarization with a warning instead of aborting.

## Sample corpus

[`transcripts/`](transcripts/) holds the transcripts of ten Itnig episodes picked at
random (reproducible seed, 10.2 h of audio, 104,233 words), as Markdown scripts and flat
JSON.
The selection criteria and the caveats about transcription quality are in
[`transcripts/README.md`](transcripts/README.md).

## Pinned versions

These pins were verified on Windows 11 with an RTX 4070; check with a real model load
before upgrading them:

- **`torch 2.8.0+cu126`** on Windows (2.13 fails to import there). The `+cu126` suffix
  matters: plain `2.8.0` lets the installer pick the CPU wheel. macOS and Linux get
  `2.8.0` from PyPI.
- **`ctranslate2 4.5.0`**: 4.8.1, the one `faster-whisper` pulls in, segfaults when
  loading any model.
- **`nvidia-cublas-cu12` / `nvidia-cudnn-cu12`** on Windows: CTranslate2 needs those
  DLLs, registered at import time before WhisperX loads.
- **`yt-dlp`** has to be kept up to date: an outdated one gets HTTP 403 from YouTube on
  every full download.

## License

The code is released under the [MIT License](LICENSE). The transcripts in
`transcripts/` are not covered by it: they come from Itnig's public videos and are
included for analysis and search purposes only; all rights to the original content
belong to Itnig.
