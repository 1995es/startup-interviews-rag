"""Numbered transcript -> LLM segmentation (step 2 of docs/ingesta-llm.md).

Reads `llm_input/<id>.txt` + `.json` and writes `segments/<id>.json`, one
LLM call per episode, skipped when a cached record matches the model and
prompt version. The provider comes from LLM_PROVIDER in .env (default
anthropic) or --provider; its API key from ANTHROPIC_API_KEY or
OPENROUTER_API_KEY.

    poetry run python video_rag/interfaces/cli/segment.py yOLw6ncCJwY          # one episode
    poetry run python video_rag/interfaces/cli/segment.py                      # all of llm_input/
    poetry run python video_rag/interfaces/cli/segment.py yOLw6ncCJwY --force  # ignore the cache
    poetry run python video_rag/interfaces/cli/segment.py yOLw6ncCJwY --provider openrouter
"""

import argparse
import logging
import sys
from dataclasses import replace
from pathlib import Path

from video_rag import container
from video_rag.application.ports.llm import DEFAULT_EFFORT, EFFORTS
from video_rag.config import Settings
from video_rag.domain.errors import VideoRagError
from video_rag.interfaces.cli._common import cli_entrypoint

log = logging.getLogger("video_rag.cli.segment")


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="llm_input/<id>.txt -> segments/<id>.json with an LLM (step 2)"
    )
    ap.add_argument("video_ids", nargs="*", help="video IDs (default: every episode in llm_input/)")
    ap.add_argument("--in-dir", default="llm_input")
    ap.add_argument("-o", "--out-dir", default="segments")
    ap.add_argument(
        "--provider",
        choices=container.LLM_PROVIDERS,
        help="LLM provider (default: LLM_PROVIDER from .env, else anthropic)",
    )
    ap.add_argument("--model", help="model id (default: the provider's default)")
    ap.add_argument("--effort", default=DEFAULT_EFFORT, choices=EFFORTS)
    ap.add_argument(
        "--force", action="store_true", help="call the LLM even if a valid cache entry exists"
    )
    return ap.parse_args()


@cli_entrypoint
def main() -> None:
    args = parse_args()
    settings = Settings.from_env()
    settings = replace(
        settings,
        llm_input_dir=Path(args.in_dir),
        segments_dir=Path(args.out_dir),
        llm_provider=args.provider or settings.llm_provider,
        llm_model=args.model or settings.llm_model,
    )
    use_case = container.segment_episode(settings)

    available = use_case.episodes()
    vids = args.video_ids or available
    if not vids:
        sys.exit(f"ERROR: no episodes in {settings.llm_input_dir} (run prepare.py first).")
    for vid in vids:
        if vid not in available:
            sys.exit(f"ERROR: {settings.llm_input_dir / vid}.txt is missing")

    failed = []
    for vid in vids:
        try:
            use_case.execute(vid, effort=args.effort, force=args.force)
        except VideoRagError as exc:
            log.info(f"{vid}: ERROR {exc}")
            failed.append(vid)

    if failed:
        sys.exit(f"{len(failed)} of {len(vids)} failed: {', '.join(failed)}")


if __name__ == "__main__":
    main()
