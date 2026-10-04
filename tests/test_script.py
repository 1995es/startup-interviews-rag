from video_rag.domain.script import ScriptOptions, clean_turns, render_script
from video_rag.domain.transcript import Turn
from video_rag.interfaces.cli.script import parse_names

TURNS = clean_turns(
    [
        Turn("  Hi   there ", "SPEAKER_00", 5, 6),
        Turn("a | b", None, 3661, 3662),
        Turn("   ", "SPEAKER_01", 7, 8),
    ]
)


def test_clean_turns_drops_empty_and_labels_unknown_speakers():
    assert [(t.speaker, t.text) for t in TURNS] == [
        ("SPEAKER_00", "Hi there"),
        ("SPEAKER_?", "a | b"),
    ]


def test_render_lines_with_names_and_timestamps():
    md = render_script(
        TURNS, ScriptOptions(title="T", timestamps=True, names=parse_names("SPEAKER_00=Ana"))
    )
    assert md == (
        "# T\n\n*2 turns · 2 speakers: Ana, SPEAKER_?*\n\n"
        "`00:00:05` **Ana** — Hi there\n\n"
        "`01:01:01` **SPEAKER_?** — a | b\n"
    )


def test_render_table_escapes_pipes():
    md = render_script(TURNS, ScriptOptions(title="T", table=True))
    assert "| Speaker | Text |\n|---|---|\n" in md
    assert "| **SPEAKER_?** | a \\| b |" in md
