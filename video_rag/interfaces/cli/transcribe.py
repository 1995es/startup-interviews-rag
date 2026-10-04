"""Transcribe and diarize a YouTube video, given its URL, with WhisperX.

    poetry run python video_rag/interfaces/cli/transcribe.py \
        "https://www.youtube.com/watch?v=..." --language en

The audio is downloaded to audio/<id>.wav (16 kHz mono), transcribed, aligned
word by word and split by speaker. A local video/audio file works too in
place of the URL.

The output, output/<id>.json by default (-o to change it), is a list of
speaking turns in order, one object per turn:

    [
      {
        "text": "So how did the company start?",
        "speaker": "SPEAKER_00",
        "start": 0.031,
        "end": 2.457
      },
      {
        "text": "It started in 2015, when we ...",
        "speaker": "SPEAKER_01",
        "start": 2.718,
        "end": 41.902
      }
    ]

- text: everything one speaker says until someone else takes over.
- speaker: the pyannote label (SPEAKER_00, SPEAKER_01, ...), not a name.
- start / end: seconds from the start of the video, rounded to milliseconds.

Speaker diarization needs HF_TOKEN (environment or .env) and accepted terms
for pyannote/speaker-diarization-3.1 on huggingface.co. Without it the audio
is still transcribed, but every turn comes out as SPEAKER_00.
"""

import argparse
from dataclasses import replace
from pathlib import Path

from video_rag import container
from video_rag.config import ConfigError, Settings
from video_rag.interfaces.cli._common import (
    add_transcription_args,
    cli_entrypoint,
    transcription_options,
)


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="YouTube URL or local file -> JSON [{text, speaker, start, end}]"
    )
    ap.add_argument("source", help="URL or path to a local video/audio file")
    ap.add_argument("-o", "--output", help="output .json (default: output/<id>.json)")
    add_transcription_args(ap)
    return ap.parse_args()


@cli_entrypoint
def main() -> None:
    args = parse_args()
    settings = Settings.from_env()
    key = None
    if args.output:
        out = Path(args.output)
        if out.suffix.lower() != ".json":
            raise ConfigError(f"--output must be a .json file, got '{out}'.")
        settings = replace(settings, transcripts_dir=out.parent)
        key = out.stem

    container.transcribe_video(settings).execute(args.source, transcription_options(args), key=key)


if __name__ == "__main__":
    main()
