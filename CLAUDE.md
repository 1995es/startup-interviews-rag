# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A RAG system over the interviews of the Itnig startup podcast (Spanish), with a
frontend on top for questions such as "how do I find my first customers?" or "how do I
validate an idea?": the answer should bring back the experiences of the founders who
talked about it, with a link to the minute in the video. The repository is public and
work in progress, so code and docs should read well to an outside reviewer.

**Current phase: ingestion.** Done: transcription with diarization (`prepare.py`),
numbered LLM input (step 1 of `docs/llm-ingestion.md`) and LLM segmentation (step 2,
`segment.py`). Next: validation (step 3), chunk building, timestamps and contextual
headers (steps 4–6). Later: BGE-M3 embeddings, Qdrant (`docker-compose.yml` is ready),
retrieval, an API and the web frontend. Keep the Roadmap table in `README.md` and the
Status table in `docs/llm-ingestion.md` in sync when a step lands.

The code is a package, `video_rag/`, with a **hexagonal (ports and adapters)
architecture**:

```
video_rag/
├── domain/          pure logic: no I/O, no third-party dependencies
├── application/
│   ├── ports/       abstract classes the use cases need
│   └── use_cases/   PrepareLLMInput, SegmentEpisode, RenderScript
├── infrastructure/  driven adapters: WhisperX, yt-dlp, Anthropic, OpenRouter, JSON
├── interfaces/
│   └── cli/         driving adapters (api/ later)
├── config.py        Settings: environment + .env
└── container.py     composition root: the only place that picks adapters
```

Dependency rule: `interfaces` → `application` → `domain`, and `infrastructure`
implements the `application` ports. Neither `domain` nor `application` imports
`infrastructure`, `interfaces`, `config` or third-party SDKs. Interfaces get their use
case from `container` and never import `infrastructure` themselves. Injection is by
constructor, by hand, with no framework.

The three scripts live in `video_rag/interfaces/cli/`. There are no installed commands
(`[project.scripts]`): they run by path, `poetry run python
video_rag/interfaces/cli/<script>.py`. The `video_rag.*` imports resolve because
`poetry install` installs the package itself into the venv in editable mode.

- `prepare.py`: step 1 of `docs/llm-ingestion.md` and the only entry point for a video
  (URLs only). A single use case, `PrepareLLMInput`: metadata (`meta/<id>.json`) → 16 kHz
  mono wav (`audio/<id>.wav`) → transcription → word alignment → diarization → turns
  (`output/<id>.json`, `[{text, speaker, start, end}]`) → `llm_input/<id>.txt` with
  numbered turns (`t020`, and `t020.s1`… for turns over 150 words) and
  `llm_input/<id>.json` with the original text of each ID. It reuses what already
  exists: `meta/<id>.json` and `output/<id>.json` (no network, no WhisperX; `--force`
  redoes them) and `audio/<id>.wav` (never re-downloaded, even with `--force`).
  Diarization turns on by itself when `HF_TOKEN` is set (environment or `.env`), and
  GPU/CPU are auto-detected.
- `script.py`: `output/<id>.json` → interview-style Markdown script, one line per turn.
  **Layout only**: it does not touch the turns.
- `segment.py`: step 2. `llm_input/<id>.txt` → one LLM call with JSON schema output →
  `segments/<id>.json` (speakers, units, glossary, episode_summary). The cache is keyed
  by `model` + `PROMPT_VERSION` (`domain/segmentation.py`). `raw_tags` are free, with no
  closed taxonomy (see step 9 of the doc).

Transcription runs **in the same process** as `prepare.py`. There used to be a separate
`transcribe.py` that `prepare.py` launched as a child process to isolate the
CTranslate2 segfault; it was merged in at the cost of that isolation. Two mitigations:
`cli_entrypoint` enables `faulthandler`, so a native crash prints the Python stack
instead of dying silently, and the recognizer is wrapped in `LazyRecognizer`, so
WhisperX/torch are only imported when there really is something to transcribe.

### LLM: the `LLMProvider` port

`application/ports/llm.py` defines `LLMProvider.generate_structured(StructuredRequest)
-> StructuredResponse`. No use case knows the SDK: adapters translate their exceptions
into `LLMError`. There are two implementations in `infrastructure/llm/`:

- `AnthropicProvider` (default, `claude-opus-5-5`): adaptive thinking, `effort` and
  `fallbacks: "default"`; the model that actually answered is stored in `served_by`.
  Opus 5.5 rejects `temperature`, so it is not pinned to 0 as the doc's original
  design said. Its API default `effort` is `medium`, so the effort is always sent.
- `OpenRouterProvider` (`anthropic/claude-opus-5-5`): the `openai` SDK against
  `https://openrouter.ai/api/v1`, with `response_format` json_schema and
  `reasoning.effort`. Token usage is normalized to Anthropic semantics: `input_tokens`
  excludes cached tokens.

The provider is chosen with `LLM_PROVIDER` in `.env` (`anthropic` | `openrouter`) or
with `--provider`; the model with `LLM_MODEL` or `--model`. Keys are read from
`ANTHROPIC_API_KEY` and `OPENROUTER_API_KEY`. Since model ids differ between providers,
switching provider segments again. To add a provider: an adapter in
`infrastructure/llm/`, a branch in `container.build_llm()` and its name in
`LLM_PROVIDERS`.

`transcripts/` is the only output folder that **is** versioned: the transcripts of ten
Itnig videos (annotated `.md` + flat `.json`) plus their index. It is regenerated with
the normal pipeline; `audio/`, `output/`, `meta/`, `llm_input/` and `segments/` stay
ignored. Not to be confused with `Settings.transcripts_dir`, which is `output/`.

`notebooks/h1_diarization_check.ipynb` is a **standalone** Colab notebook (it does not
clone the repo) to test hypothesis H1: compare pyannote's overlapping diarization with
its exclusive one. It installs with `pip` into Colab's own Python, like any WhisperX
demo: **no venv, no lock**. Only `whisperx` is pinned, to the `poetry.lock` version;
yt-dlp is left unpinned, because an old one is what breaks YouTube downloads. A separate
venv inherited the kernel's environment
(`MPLBACKEND=module://matplotlib_inline.backend_inline`) without its packages, and the
lock's versions (meant for Windows: `ctranslate2 4.5.0`, `nltk 3.10.3`) added nothing on
Colab and broke things. It carries `video_rag/` embedded as a base64 tar.gz and
`h1_check.py` as is; it also downloads NLTK's `punkt_tab`, because recent NLTK versions
refuse downloads through a proxy and Colab uses one. It is generated by
`notebooks/build_h1_notebook.py`: do not edit the `.ipynb` by hand, and **rebuild it
after any change under `video_rag/`** (even a comment): `tests/test_notebook.py` fails
when it is stale.

Dependencies are managed with **Poetry** (`pyproject.toml` + `poetry.lock`; there is
no `requirements.txt`). `poetry.toml` keeps the venv inside the project, in `.venv/`.
Everything runs through `poetry run`. A new script is a module in `interfaces/cli/`
with its own `main()` and `if __name__ == "__main__"`. To add a dependency, use
`poetry add <package>`, never `pip install`. Python 3.11–3.12: `ctranslate2 4.5.0` has
no wheels for 3.13.

## Commands

```bash
# LLM ingestion (steps 1 and 2). Step 1 also writes output/<id>.json
poetry run python video_rag/interfaces/cli/prepare.py "https://www.youtube.com/watch?v=..." --language es --min-speakers 2
poetry run python video_rag/interfaces/cli/segment.py <id> [--provider openrouter] [--model ...] [--force]

# output/<id>.json -> Markdown script
poetry run python video_rag/interfaces/cli/script.py output/<id>.json --timestamps

# Fast iteration on the transcript: small model, redoes output/<id>.json
# (the wav in audio/ is reused, not downloaded again)
poetry run python video_rag/interfaces/cli/prepare.py "https://www.youtube.com/watch?v=..." --model tiny --language es --force

# Rebuild the Colab notebook after changing video_rag/ or h1_check.py
poetry run python notebooks/build_h1_notebook.py

# Tests (domain, use cases with fakes, LLM adapters with stub clients)
poetry run pytest

# Format and lint (config in [tool.ruff] of pyproject.toml)
poetry run ruff format .
poetry run ruff check . --fix
```

Tests never touch the network or models: `tests/fakes.py` has in-memory adapters for
the ports, and the LLM adapters are tested with stub clients injected through the
constructor.

## Environment constraints (verified, do not change lightly)

These versions are pinned in `pyproject.toml` because the alternatives **break on the
Windows machine** (Win 11, RTX 4070). Before "upgrading dependencies", verify with a
real model load:

- `torch 2.8.0+cu126`. 2.13 fails to import (`WinError 1114` loading `c10.dll`), also
  in the system's Anaconda install.
- The `+cu126` suffix is mandatory in the pin: with `torch==2.8.0` pip accepts the
  `+cpu` wheel and `torch.cuda.is_available()` turns `False`. In `pyproject.toml` it is
  a multiple constraint: `+cu126` from the `pytorch-cu126` source on Windows, and PyPI's
  `2.8.0` elsewhere.
- The markers use `platform_system == 'Windows'`, not `sys_platform == 'win32'`: torch
  declares its `nvidia-*` packages with `platform_system == "Linux"` and Poetry does not
  know `sys_platform` and `platform_system` are mutually exclusive, so with
  `sys_platform` locking fails on a cuDNN version conflict.
- `ctranslate2 4.5.0`. 4.8.1 (the one `faster-whisper` pulls in) segfaults (exit 139)
  when loading any model, even on CPU.
- `nvidia-cublas-cu12` / `nvidia-cudnn-cu12` are installed because CTranslate2 needs
  those DLLs on Windows.

When debugging crashes: a pipe (`| tail`) swallows the exit code and the buffered
output of a process that dies abruptly. Use `PYTHONUNBUFFERED=1` and `${PIPESTATUS[0]}`;
that is how the silent "exit 0" turned out to be a CTranslate2 segfault.

## Design details that a quick read misses

**`_register_cuda_dlls()` runs when
`infrastructure/transcription/whisperx_recognizer.py` is imported, before whisperx.** It
registers `torch/lib` and `site-packages/nvidia/*/bin` as DLL directories. Without it
CTranslate2 cannot find cuDNN/cuBLAS on Windows. Do not move that call below the
whisperx imports, which for that same reason are local, inside `recognize()`. For the
same reason, `container.py` imports the heavy adapters (WhisperX, the LLM SDKs) inside
each factory rather than at module top, and the WhisperX one also behind
`LazyRecognizer`: on Windows that import already loads torch.

**Speaker turns are cut per word, not per segment.** A Whisper segment lasts ~20 s and
usually contains question and answer, so grouping by segment speaker destroys the
dialogue (643 fake turns vs. 547 real ones in the sample video). `build_turns()`
(`domain/turns.py`) rebuilds turns from each word's speaker and applies two chained
fixes: `smooth_runs()` absorbs runs shorter than `--min-words` words (diarization flips
speaker on isolated words) and `snap_to_sentences()` moves the cut to the nearest
sentence end (±3 words) so sentences are not split. If the JSON has no word timings it
falls back to one row per segment.

**The YouTube download retries with several format strings** (`bestaudio/best` →
`251/140/bestaudio` → `18/best`, in `infrastructure/audio/ytdlp_audio_source.py`). The
original notebook's `bestaudio/best` got 403 from YouTube; do not simplify that loop.
That loop does **not** save an outdated yt-dlp: with 2026.7.4 YouTube returned 403 on
any full download, with all three strings and every `player_client` (`tv_embedded`,
`android`, `ios`…). Telltale symptom: `--list-formats` works and even a 10 kB `--test`
passes, but the full download dies with 403. The fix is upgrading yt-dlp, not touching
the code.

**Cascading degradation**: if the model fails to load on the GPU it is retried on
CPU/int8; without `HF_TOKEN` it warns and continues without diarization. The pipeline
should never abort for lack of diarization.

## Conventions

- **Everything is written in English**: code (identifiers, comments, docstrings,
  `print`/`log` messages, `--help` texts, errors and fixed literals a script writes,
  e.g. header labels) and documentation (`README.md`, `CLAUDE.md`, `docs/`). This
  applies to new files and to any line added or modified in existing ones.
- Spanish is only for **data**: the transcribed content, the data values of the
  segmentation prompt (`UNIT_TYPES`, `ROLES`, the tag and question examples), what the
  LLM generates (titles, summaries, tags, questions) and the Markdown transcripts in
  `transcripts/`. When docs quote Spanish data, add an English gloss. The fixed labels
  that `script.py` adds ("turns", "speakers", "Time"…) are in English; the already
  versioned `.md` files in `transcripts/` keep the old Spanish ones until they are
  regenerated.
- `print`/`log` output has no non-ASCII characters, because of the Windows console's
  cp1252.
- Code passes `ruff format` and `ruff check` (100-column lines; rules E, W, F, I, B,
  UP, SIM). Run both, plus `pytest`, before calling a change done.
- Generated files (`audio/`, `output/`, `meta/`, `llm_input/`, `segments/`) are not
  source: they can be regenerated and must not be edited by hand.
