from video_rag.domain.transcript import TranscriptSegment, Turn, Word
from video_rag.domain.turns import build_turns


def words(*specs: tuple[str, str]) -> list[Word]:
    return [Word(text=t, speaker=s, start=float(i), end=i + 0.5) for i, (t, s) in enumerate(specs)]


def test_cuts_turns_per_word_not_per_segment():
    seg = TranscriptSegment(
        text="",
        speaker="A",
        words=words(
            ("How", "A"),
            ("did", "A"),
            ("it", "A"),
            ("start?", "A"),
            ("With", "B"),
            ("my", "B"),
            ("own", "B"),
            ("boat.", "B"),
        ),
    )
    turns = build_turns([seg], min_words=2)
    assert [(t.speaker, t.text) for t in turns] == [
        ("A", "How did it start?"),
        ("B", "With my own boat."),
    ]
    assert (turns[0].start, turns[1].end) == (0.0, 7.5)


def test_absorbs_short_speaker_flips():
    seg = TranscriptSegment(
        text="",
        words=words(("one", "A"), ("two", "A"), ("three", "B"), ("four", "A"), ("five.", "A")),
    )
    turns = build_turns([seg], min_words=2)
    assert [(t.speaker, t.text) for t in turns] == [("A", "one two three four five.")]


def test_snaps_boundary_to_sentence_end():
    # The diarizer switches to B one word too late: "Yes" opens B's answer,
    # so the boundary moves back to the nearest sentence end, "start?".
    seg = TranscriptSegment(
        text="",
        words=words(
            ("How", "A"),
            ("did", "A"),
            ("it", "A"),
            ("start?", "A"),
            ("Yes", "A"),
            ("it", "B"),
            ("did.", "B"),
            ("Really.", "B"),
        ),
    )
    turns = build_turns([seg], min_words=1)
    assert [t.text for t in turns] == ["How did it start?", "Yes it did. Really."]


def test_leading_words_take_the_first_diarized_speaker():
    seg = TranscriptSegment(text="", words=words(("So", None), ("well", None), ("yes.", "B")))
    assert build_turns([seg], min_words=1) == [Turn("So well yes.", "B", 0.0, 2.5)]


def test_falls_back_to_segments_without_word_timings():
    segs = [
        TranscriptSegment(text=" Hello. ", speaker=None, start=0.0, end=1.0),
        TranscriptSegment(text="  ", speaker="B"),
    ]
    assert build_turns(segs, min_words=4) == [Turn("Hello.", "SPEAKER_00", 0.0, 1.0)]
