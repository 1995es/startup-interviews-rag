"""Replays the segments that h1_check.py saves (<id>.<variant>.segments.json:
each word with its diarization speaker, before turn building) through
build_turns with several --min-words values, and prints where the turns
differ from the baseline. It chooses the default without rerunning
transcription or diarization, so it runs locally without a GPU:

    poetry run python notebooks/min_words_diff.py output/yOLw6ncCJwY.overlapping.segments.json
    poetry run python notebooks/min_words_diff.py <segments.json> --baseline 4 --candidates 2 3
"""

import argparse
import difflib
import json
from pathlib import Path

from startup_interviews_rag.domain.transcript import TranscriptSegment, Turn, Word
from startup_interviews_rag.domain.turns import build_turns

SHORT_TURN = 4  # words; what the current default treats as a speaker flip


def load_segments(path: Path) -> list[TranscriptSegment]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return [
        TranscriptSegment(**{**seg, "words": [Word(**w) for w in seg["words"]]}) for seg in data
    ]


def diff_regions(base: list[Turn], other: list[Turn]) -> list[tuple[list[Turn], list[Turn]]]:
    """The stretches where the two turn lists disagree, as (base, other)."""
    matcher = difflib.SequenceMatcher(
        a=[(t.speaker, t.text) for t in base],
        b=[(t.speaker, t.text) for t in other],
        autojunk=False,
    )
    return [
        (base[i1:i2], other[j1:j2])
        for tag, i1, i2, j1, j2 in matcher.get_opcodes()
        if tag != "equal"
    ]


def short_turns(turns: list[Turn]) -> int:
    return sum(len(t.text.split()) < SHORT_TURN for t in turns)


def fmt(turn: Turn, width: int) -> str:
    # Changes usually sit at either end of a long turn: keep both ends.
    text = turn.text
    if len(text) > width:
        half = (width - 5) // 2
        text = f"{text[:half]} ... {text[-half:]}"
    start = "?" if turn.start is None else f"{turn.start:8.2f}"
    end = "?" if turn.end is None else f"{turn.end:8.2f}"
    return f"{start}-{end} {turn.speaker}: {text}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("segments", type=Path, help="<id>.<variant>.segments.json")
    parser.add_argument("--baseline", type=int, default=4, help="min_words to compare against")
    parser.add_argument("--candidates", type=int, nargs="+", default=[1, 2, 3])
    parser.add_argument("--width", type=int, default=180, help="max characters per turn")
    args = parser.parse_args()

    segments = load_segments(args.segments)
    base = [t.rounded() for t in build_turns(segments, args.baseline)]

    summary = [(args.baseline, len(base), short_turns(base), 0)]
    for k in args.candidates:
        turns = [t.rounded() for t in build_turns(segments, k)]
        regions = diff_regions(base, turns)
        summary.append((k, len(turns), short_turns(turns), len(regions)))
        print(f"\n===== min_words={k} vs {args.baseline}: {len(regions)} regions differ =====")
        for old, new in regions:
            print()
            for t in old:
                print(f"  - {fmt(t, args.width)}")
            for t in new:
                print(f"  + {fmt(t, args.width)}")

    print(f"\n{'min_words':>9} {'turns':>6} {f'<{SHORT_TURN} words':>10} {'regions':>8}")
    for k, n, short, regions in sorted(summary):
        print(f"{k:>9} {n:>6} {short:>10} {regions:>8}")


if __name__ == "__main__":
    main()
