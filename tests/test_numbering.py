from startup_interviews_rag.domain.numbering import build_llm_input, number_turns
from startup_interviews_rag.domain.transcript import Turn
from startup_interviews_rag.domain.video import VideoMeta, video_id


def test_short_turns_keep_one_id_and_long_ones_split_into_sentences():
    turns = [
        Turn("Hi there.", "SPEAKER_00", 0, 2),
        Turn("First one. Second one? Third!", None, 75, 90),
    ]
    lines, units = number_turns(turns, max_words=3)
    assert lines == [
        "[t001 00:00:00 SPEAKER_00] Hi there.",
        "[t002 00:01:15 SPEAKER_00]",
        "[t002.s1] First one.",
        "[t002.s2] Second one?",
        "[t002.s3] Third!",
    ]
    assert [u.id for u in units] == ["t001", "t002.s1", "t002.s2", "t002.s3"]
    assert {u.turn for u in units[1:]} == {"t002"}


def test_llm_input_has_header_and_speakers():
    meta = VideoMeta.from_info({"id": "abc", "title": "T", "upload_date": "20200107"})
    llm_input = build_llm_input(meta, [Turn("Hola.", "SPEAKER_01", 1, 2)], 150)
    assert llm_input.prompt.startswith("# Episode\n\nTitle: T\nDate: 2020-01-07\n")
    assert llm_input.prompt.endswith("# Transcript\n\n[t001 00:00:01 SPEAKER_01] Hola.\n")
    assert llm_input.speaker_labels == ["SPEAKER_01"]
    assert llm_input.split_turns == 0


def test_video_id_from_url_variants():
    assert video_id("https://www.youtube.com/watch?v=yOLw6ncCJwY&t=3") == "yOLw6ncCJwY"
    assert video_id("https://youtu.be/yOLw6ncCJwY") == "yOLw6ncCJwY"
    assert video_id("https://example.com/video") is None
