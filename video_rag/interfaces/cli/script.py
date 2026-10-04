"""Flat transcript JSON -> Markdown script, one row per turn.

    poetry run python video_rag/interfaces/cli/script.py output/2vv4hHAvqnE.json --timestamps
    poetry run python video_rag/interfaces/cli/script.py output/2vv4hHAvqnE.json \
        --names SPEAKER_00=Jordi,SPEAKER_01=Marc
    poetry run python video_rag/interfaces/cli/script.py output/2vv4hHAvqnE.json \
        --table --title "Itnig roundtable"
"""

import argparse
from dataclasses import replace
from pathlib import Path

from video_rag import container
from video_rag.config import Settings
from video_rag.domain.script import ScriptOptions
from video_rag.interfaces.cli._common import cli_entrypoint


def parse_names(raw: str | None) -> dict[str, str]:
    """'SPEAKER_00=Jordi,SPEAKER_01=Marc' -> {'SPEAKER_00': 'Jordi', ...}"""
    names = {}
    for pair in (raw or "").split(","):
        if "=" in pair:
            k, v = pair.split("=", 1)
            names[k.strip()] = v.strip()
    return names


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description="Turns the pipeline's flat JSON into a Markdown script."
    )
    ap.add_argument("json_path", help=".json file written by transcribe.py")
    ap.add_argument("-o", "--output", default=None, help="output file (default: <name>.guion.md)")
    ap.add_argument("--title", default=None, help="document title")
    ap.add_argument("--timestamps", action="store_true", help="add timestamps")
    ap.add_argument("--table", action="store_true", help="output as a Markdown table")
    ap.add_argument(
        "--names", default=None, help="rename speakers: SPEAKER_00=Jordi,SPEAKER_01=Marc"
    )
    return ap.parse_args()


@cli_entrypoint
def main() -> None:
    args = parse_args()
    src = Path(args.json_path)
    settings = replace(Settings.from_env(), transcripts_dir=src.parent)

    options = ScriptOptions(
        title=args.title or f"Transcript — {src.stem}",
        timestamps=args.timestamps,
        table=args.table,
        names=parse_names(args.names),
    )
    script = container.render_script(settings).execute(src.stem, options)
    if not script.has_speakers:
        print(
            "WARNING: the JSON has no speaker labels. Regenerate it with "
            "HF_TOKEN set to separate speakers."
        )

    out_path = Path(args.output) if args.output else src.with_suffix(".guion.md")
    out_path.write_text(script.markdown, encoding="utf-8")
    print(f"{script.turns} turns -> {out_path}")


if __name__ == "__main__":
    main()
