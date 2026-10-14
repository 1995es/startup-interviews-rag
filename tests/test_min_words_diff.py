"""min_words_diff.py replays the segments h1_check.py saves: it must read
them back exactly and point at the turns a lower --min-words changes."""

import importlib.util
import json
from dataclasses import asdict
from pathlib import Path

from startup_interviews_rag.domain.transcript import TranscriptSegment, Turn, Word
from startup_interviews_rag.domain.turns import build_turns

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location("diff", ROOT / "notebooks/min_words_diff.py")
diff = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(diff)

HOST, GUEST = "SPEAKER_02", "SPEAKER_01"


def said(speaker: str, text: str) -> list[tuple[str, str]]:
    return [(word, speaker) for word in text.split()]


# Words of yOLw6ncCJwY at 142-152 s as diarized on Colab: pyannote only gives
# the host "Esto tiene" of his "¡Ostras! Esto tiene mérito, ¿eh? ¿Y cómo...?".
WINDOW = (
    said(HOST, "¿Ah, sí? Sí. ¿Y es lo que")
    + said(GUEST, "hiciste? Sí. Y con una niña de dos años. ¡Ostras!")
    + said(HOST, "Esto tiene")
    + said(GUEST, "mérito, ¿eh? ¿Y cómo...? Bueno, siempre se dice, ¿no?")
)


def window_segments() -> list[TranscriptSegment]:
    words = [Word(text, speaker, float(i), i + 0.5) for i, (text, speaker) in enumerate(WINDOW)]
    return [TranscriptSegment(text="", speaker=GUEST, start=0.0, end=len(words), words=words)]


def test_reads_back_what_h1_check_saves(tmp_path):
    segments = window_segments()
    path = tmp_path / "x.overlapping.segments.json"
    path.write_text(json.dumps([asdict(s) for s in segments], ensure_ascii=False))
    assert diff.load_segments(path) == segments


def test_lower_min_words_recovers_the_host_interjection():
    base = build_turns(window_segments(), 4)
    lower = build_turns(window_segments(), 2)

    [(old, new)] = diff.diff_regions(base, lower)
    assert [t.speaker for t in old] == [GUEST]
    assert [(t.speaker, t.text) for t in new] == [
        (GUEST, "Sí. Y con una niña de dos años. ¡Ostras!"),
        (HOST, "Esto tiene mérito, ¿eh?"),
        (GUEST, "¿Y cómo...? Bueno, siempre se dice, ¿no?"),
    ]
    assert diff.short_turns(base) == 0


def test_long_turns_keep_both_ends():
    turn = Turn("Sí. Y con una niña de dos años. ¡Ostras! Esto tiene mérito", GUEST, 144.6, 148.7)
    line = diff.fmt(turn, 30)
    assert line.startswith("  144.60-  148.70 SPEAKER_01: Sí. Y con")
    assert " ... " in line
    assert line.endswith("tiene mérito")
