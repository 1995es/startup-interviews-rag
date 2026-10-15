from startup_interviews_rag.domain.numbering import build_llm_input
from startup_interviews_rag.domain.transcript import Turn
from startup_interviews_rag.domain.validation import validate_segmentation
from startup_interviews_rag.domain.video import VideoMeta


def words(n: int) -> str:
    return " ".join(["palabra"] * n)


# t001-t004 are 50-word turns; t005 is a 700-word turn split into t005.s1-s2.
LLM_INPUT = build_llm_input(
    VideoMeta(id="vid"),
    [Turn(words(50) + ".", f"SPEAKER_0{i % 2}", i, i + 1) for i in range(4)]
    + [Turn(f"{words(350)}. {words(350)}.", "SPEAKER_01", 4, 5)],
    150,
)
SPEAKERS = [{"label": "SPEAKER_00"}, {"label": "SPEAKER_01"}]


def unit(from_id: str, to_id: str, type_: str = "anecdota") -> dict:
    return {"from": from_id, "to": to_id, "type": type_}


def response(*units: dict, speakers: list[dict] = SPEAKERS) -> dict:
    return {"speakers": speakers, "units": list(units)}


def test_a_valid_segmentation_has_no_errors():
    valid = response(unit("t001", "t002"), unit("t003", "t005.s1"), unit("t005.s2", "t005.s2"))
    assert validate_segmentation(valid, LLM_INPUT) == []


def test_ids_must_exist_and_a_split_turn_is_cut_by_its_sentences():
    bad = response(unit("t001", "t002"), unit("t003", "t005"), unit("t009", "t009"))
    errors = validate_segmentation(bad, LLM_INPUT)
    assert (
        "unit 2: `to` t005 is not a valid ID (t005 is split into sentences: t005.s1-t005.s2)"
        in errors
    )
    assert "unit 3: `from` t009 is not a valid ID" in errors
    assert "unit 3: `to` t009 is not a valid ID" in errors


def test_from_must_not_come_after_to():
    bad = response(unit("t001", "t002"), unit("t004", "t003"), unit("t005.s1", "t005.s2"))
    assert "unit 2: `from` t004 comes after `to` t003" in validate_segmentation(bad, LLM_INPUT)


def test_every_id_belongs_to_exactly_one_unit():
    bad = response(unit("t002", "t003"), unit("t003", "t004"), unit("t005.s2", "t005.s2"))
    errors = validate_segmentation(bad, LLM_INPUT)
    assert "not covered by any unit: t001, t005.s1" in errors
    assert "covered by more than one unit: t003" in errors


def test_units_must_follow_the_transcript_order():
    bad = response(unit("t003", "t005.s1"), unit("t001", "t002"), unit("t005.s2", "t005.s2"))
    assert "unit 2 (t001-t002) starts before unit 1 (t003-t005.s1)" in validate_segmentation(
        bad, LLM_INPUT
    )


def test_units_hold_80_to_600_words_except_filler():
    bad = response(unit("t001", "t001"), unit("t002", "t004"), unit("t005.s1", "t005.s2"))
    assert validate_segmentation(bad, LLM_INPUT) == [
        "unit 1 (t001-t001, anecdota) has 50 words; it must have 80-600 (only relleno is exempt)",
        "unit 3 (t005.s1-t005.s2, anecdota) has 700 words; it must have 80-600 "
        "(only relleno is exempt)",
    ]
    filler = response(
        unit("t001", "t001", "relleno"),
        unit("t002", "t004"),
        unit("t005.s1", "t005.s1"),
        unit("t005.s2", "t005.s2"),
    )
    assert validate_segmentation(filler, LLM_INPUT) == []


def test_every_speaker_label_is_described():
    valid_units = (unit("t001", "t002"), unit("t003", "t005.s1"), unit("t005.s2", "t005.s2"))
    bad = response(*valid_units, speakers=[{"label": "SPEAKER_01"}])
    assert validate_segmentation(bad, LLM_INPUT) == ["`speakers` is missing SPEAKER_00"]
