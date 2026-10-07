"""Builds notebooks/h1_diarization_check.ipynb, a standalone Colab notebook
that runs h1_check.py on a free T4 GPU without cloning the repo.

It installs into Colab's own Python with pip, like any WhisperX demo: no
venv, no lock file. Only whisperx is pinned (to the poetry.lock version,
the API h1_check.py is written against); yt-dlp is left unpinned because an
old one is what breaks YouTube downloads. numpy and opentelemetry get
ceilings so pip does not upgrade them past what Colab's numba and
google-adk accept, and gradio and diffusers are uninstalled because they
need a huggingface-hub that whisperx rejects. The startup_interviews_rag package goes inside
the notebook as a base64 tar.gz, so rerun this after changing it:

    poetry run python notebooks/build_h1_notebook.py
"""

import base64
import gzip
import io
import json
import tarfile
import textwrap
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NOTEBOOK = ROOT / "notebooks" / "h1_diarization_check.ipynb"
H1_SCRIPT = ROOT / "notebooks" / "h1_check.py"
VIDEO_ID = "yOLw6ncCJwY"
B64_LINE = 88  # keeps the embedded lines under ruff's 100 columns


def whisperx_version() -> str:
    lock = tomllib.loads((ROOT / "poetry.lock").read_text(encoding="utf-8"))
    return next(p["version"] for p in lock["package"] if p["name"] == "whisperx")


def package_b64() -> str:
    """startup_interviews_rag/ as a reproducible tar.gz: same sources, same bytes."""
    buf = io.BytesIO()
    with (
        gzip.GzipFile(fileobj=buf, mode="wb", mtime=0) as gz,
        tarfile.open(fileobj=gz, mode="w") as tar,
    ):
        for path in sorted((ROOT / "startup_interviews_rag").rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            data = path.read_bytes()
            info = tarfile.TarInfo(path.relative_to(ROOT).as_posix())
            info.size, info.mode = len(data), 0o644
            tar.addfile(info, io.BytesIO(data))
    return base64.b64encode(buf.getvalue()).decode("ascii")


def md(text: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": _lines(text)}


def code(text: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": _lines(text),
    }


def _lines(text: str) -> list[str]:
    return textwrap.dedent(text).strip("\n").splitlines(keepends=True)


def cells() -> list[dict]:
    b64 = package_b64()
    chunks = "\n".join(f'    "{b64[i : i + B64_LINE]}"' for i in range(0, len(b64), B64_LINE))
    return [
        md(f"""
            # H1 check: overlapping vs. exclusive speaker diarization

            Part of **startup-interviews-rag**, a pipeline that turns long-form interview
            videos (the Spanish startup podcast by Itnig) into speaker-attributed transcripts
            and then into chunks for a RAG system. Transcription and diarization run on
            [WhisperX](https://github.com/m-bain/whisperX) +
            [pyannote](https://github.com/pyannote/pyannote-audio).

            ## The problem

            In video `{VIDEO_ID}`, around 2:27, the host (Bernat) interjects *"¡Ostras! Esto
            tiene mérito, ¿eh? ¿Y cómo...?"*, but the transcript attributes it to the guest
            (Octavi). A wrong speaker there breaks the question/answer structure that the
            later chunking relies on.

            ## Hypotheses

            - **H1**: pyannote does detect Bernat, but as speech *overlapping* Octavi's.
              WhisperX assigns each word the speaker with the largest time overlap using
              pyannote's `speaker_diarization` output (which keeps overlaps), so Bernat's
              words tie with Octavi's and Octavi wins. If so, pyannote's
              `exclusive_speaker_diarization` (one speaker at a time) fixes it.
            - **H2**: pyannote does not detect the speaker change at all. Then the exclusive
              output does not help either, and the fix has to come from somewhere else.

            ## What this notebook does

            It downloads the audio, transcribes and aligns it once, diarizes it once, and
            assigns word speakers with **both** pyannote outputs. For the 144-152 s window
            it prints the raw pyannote intervals, every word with its speaker and the
            resulting turns, so the two variants can be compared side by side.

            It is self-contained (the project code is embedded, nothing is cloned) and runs
            on Colab's own Python. Total time on a T4: about 15 minutes.

            ## Before running

            1. *Runtime → Change runtime type → **T4 GPU***.
            2. Create a Hugging Face token and add it in 🔑 *Secrets* as `HF_TOKEN`, with
               notebook access enabled.
            3. With that same account, accept the terms of
               [`pyannote/speaker-diarization-community-1`](https://huggingface.co/pyannote/speaker-diarization-community-1)
               (the diarization model WhisperX {whisperx_version()} uses).

            Then *Runtime → Run all*.
            """),
        md("""
            ## 1. Install

            Into Colab's own Python. Two ceilings keep pip from breaking packages Colab
            ships: `numpy<2.3` for numba, and `opentelemetry-*<=1.42.1` for google-adk
            (pyannote pulls both in, and pip would otherwise take the latest).

            gradio and diffusers are uninstalled first: they need `huggingface-hub>=1` and
            WhisperX needs `<1`, so no version satisfies both. Neither is used here, and the
            runtime is thrown away afterwards.
            """),
        code(f"""
            !nvidia-smi -L
            !pip uninstall -q -y gradio diffusers
            !pip install -q whisperx=={whisperx_version()} yt-dlp python-dotenv \\
                "numpy<2.3" "opentelemetry-api<=1.42.1" "opentelemetry-sdk<=1.42.1"
            """),
        md("""
            ## 2. Project code

            The `startup_interviews_rag` package, embedded as a compressed archive because the
            repository is not cloned. The check uses its turn-building logic (`build_turns`), so the
            turns printed below are exactly what the pipeline would produce.
            """),
        code(
            '# @title Embedded startup_interviews_rag package { display-mode: "form" }\n'
            "import base64\n"
            "import io\n"
            "import os\n"
            "import tarfile\n\n"
            'WORKDIR = "/content/startup-interviews-rag"\n'
            f"PACKAGE = (\n{chunks}\n)\n"
            "os.makedirs(WORKDIR, exist_ok=True)\n"
            "archive = io.BytesIO(base64.b64decode(PACKAGE))\n"
            'with tarfile.open(fileobj=archive, mode="r:gz") as tar:\n'
            '    tar.extractall(WORKDIR, filter="data")\n'
            "%cd {WORKDIR}\n"
        ),
        md("""
            ## 3. Configuration

            The Hugging Face token goes into the environment, where the project reads it.

            WhisperX also needs NLTK's `punkt_tab` sentence tokenizer and downloads it on
            first use, but recent NLTK versions refuse any download through a proxy (an SSRF
            protection), and Colab goes through one. It is fetched here instead.
            """),
        code("""
            import urllib.request
            import zipfile
            from pathlib import Path

            from google.colab import userdata

            os.environ["HF_TOKEN"] = userdata.get("HF_TOKEN")

            NLTK_DATA = Path(WORKDIR) / "nltk_data"
            PUNKT_TAB = (
                "https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/tokenizers/punkt_tab.zip"
            )
            tokenizers = NLTK_DATA / "tokenizers"
            if not (tokenizers / "punkt_tab").is_dir():
                with urllib.request.urlopen(PUNKT_TAB) as response:
                    zipfile.ZipFile(io.BytesIO(response.read())).extractall(tokenizers)
            os.environ["NLTK_DATA"] = str(NLTK_DATA)
            """),
        md(f"""
            ## 4. Audio

            The whole episode (47 min), not a clip: diarization with only a minute of
            context clusters voices much worse, and the error showed up on the full video.

            If YouTube blocks the download from Colab (*"Sign in to confirm you're not a
            bot"*), upload `{VIDEO_ID}.wav` (16 kHz mono) to
            `/content/startup-interviews-rag/audio/` and run the next cells.
            """),
        code(f"""
            import yt_dlp

            VIDEO_ID = "{VIDEO_ID}"
            AUDIO = f"audio/{{VIDEO_ID}}.wav"

            if not Path(AUDIO).exists():
                opts = {{
                    "format": "bestaudio/best",
                    "outtmpl": "audio/%(id)s.%(ext)s",
                    "postprocessors": [{{"key": "FFmpegExtractAudio", "preferredcodec": "wav"}}],
                    "postprocessor_args": ["-ar", "16000", "-ac", "1"],
                    "quiet": True,
                }}
                with yt_dlp.YoutubeDL(opts) as ydl:
                    ydl.download([f"https://www.youtube.com/watch?v={{VIDEO_ID}}"])
            print(AUDIO, Path(AUDIO).stat().st_size // 1_000_000, "MB")
            """),
        md("""
            ## 5. The check

            `notebooks/h1_check.py` from the repository, written to disk as is. The window
            144-152 s covers *"Sí. Y con una niña de dos años. ¡Ostras! Esto tiene mérito,
            ¿eh? ¿Y cómo...?"*. It takes about 10 minutes: `large-v2` transcription,
            alignment and diarization of the full episode.
            """),
        code("%%writefile h1_check.py\n" + H1_SCRIPT.read_text(encoding="utf-8")),
        code("""
            T0, T1 = 144, 152
            !python h1_check.py {AUDIO} {T0} {T1}
            """),
        md("## 6. Summary and downloads"),
        code("""
            import json

            from google.colab import files

            for name in ("overlapping", "exclusive"):
                path = f"output/{VIDEO_ID}.{name}.json"
                turns = json.loads(Path(path).read_text(encoding="utf-8"))
                speakers = sorted({t["speaker"] for t in turns})
                print(f"{name:12} {len(turns):4} turns  {', '.join(speakers)}")
                files.download(path)
            """),
        md("""
            ## How to read the results

            `SPEAKER_xx` labels are numbered by pyannote on every run, so check which one is
            Bernat first: he is the one saying *"¿Y es lo que hiciste?"* just before the
            window.

            - **H1 confirmed**: in `overlapping` there is a Bernat interval overlapping one
              of Octavi's around 147-150 s, and in `exclusive` *"¡Ostras! Esto tiene mérito,
              ¿eh?"* carries Bernat's label and comes out as a turn of its own.
            - **H2**: in `overlapping` there is no Bernat interval in that window at all.

            If H1 holds, the fix in the pipeline is to assign word speakers from
            `exclusive_speaker_diarization` instead of `speaker_diarization`.
            """),
    ]


def build() -> dict:
    return {
        "cells": cells(),
        "metadata": {
            "accelerator": "GPU",
            "colab": {"gpuType": "T4", "provenance": []},
            "kernelspec": {"display_name": "Python 3", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 0,
    }


def render(notebook: dict) -> str:
    return json.dumps(notebook, indent=1, ensure_ascii=False) + "\n"


def main() -> None:
    notebook = build()
    NOTEBOOK.write_text(render(notebook), encoding="utf-8")
    print(f"{NOTEBOOK.relative_to(ROOT)}: {len(notebook['cells'])} cells")


if __name__ == "__main__":
    main()
