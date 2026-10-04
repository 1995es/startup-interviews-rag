"""YouTube URL -> input for the segmentation LLM (step 1 of docs/ingesta-llm.md).

1. Video metadata (as `yt-dlp --dump-json`, without downloading) into
   `meta/<id>.json`.
2. Turn-level transcript into `output/<id>.json`, transcribed in a child
   process. Both are reused if they already exist (no network, no WhisperX);
   `--force` redoes them.
3. Turn and sentence numbering into `llm_input/<id>.txt`, plus
   `llm_input/<id>.json` with every cuttable ID and its original text.

    poetry run python video_rag/interfaces/cli/prepare.py \
        "https://www.youtube.com/watch?v=..." --language es --min-speakers 2
"""

import argparse
from dataclasses import replace
from pathlib import Path

from video_rag import container
from video_rag.config import Settings
from video_rag.domain.numbering import DEFAULT_MAX_TURN_WORDS
from video_rag.interfaces.cli._common import (
    add_transcription_args,
    cli_entrypoint,
    transcription_options,
)


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="YouTube URL -> numbered LLM input (step 1)")
    ap.add_argument("url", help="video URL")
    ap.add_argument(
        "-o", "--out-dir", default="llm_input", help="output folder (default: llm_input/)"
    )
    ap.add_argument(
        "--max-turn-words",
        type=int,
        default=DEFAULT_MAX_TURN_WORDS,
        help="longer turns are split into sentences",
    )
    ap.add_argument(
        "--force",
        action="store_true",
        help="refetch metadata and re-transcribe even if meta/<id>.json and output/<id>.json exist",
    )
    # Passed through to the transcription as-is
    add_transcription_args(ap)
    return ap.parse_args()


@cli_entrypoint
def main() -> None:
    args = parse_args()
    settings = replace(Settings.from_env(), llm_input_dir=Path(args.out_dir))
    container.prepare_llm_input(settings).execute(
        args.url,
        transcription_options(args),
        max_turn_words=args.max_turn_words,
        force=args.force,
    )


if __name__ == "__main__":
    main()
