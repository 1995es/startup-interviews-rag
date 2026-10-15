import pytest

from fakes import FakeLLMProvider, MemoryLLMInputRepository, MemorySegmentationRepository
from startup_interviews_rag.application.ports.llm import LLMError
from startup_interviews_rag.application.ports.repositories import StorageError
from startup_interviews_rag.application.use_cases.segment_episode import SegmentEpisode
from startup_interviews_rag.domain.numbering import build_llm_input
from startup_interviews_rag.domain.segmentation import PROMPT_VERSION, SYSTEM_PROMPT
from startup_interviews_rag.domain.transcript import Turn
from startup_interviews_rag.domain.video import VideoMeta

LLM_INPUT = build_llm_input(
    VideoMeta(id="vid"),
    [Turn("Hola.", "SPEAKER_01", 0, 1), Turn("Adiós.", "SPEAKER_00", 1, 2)],
    150,
)
SPEAKERS = [{"label": "SPEAKER_00"}, {"label": "SPEAKER_01"}]
# Valid: one filler unit (exempt from the size limit) covering both turns.
RESPONSE = {
    "speakers": SPEAKERS,
    "units": [{"from": "t001", "to": "t002", "type": "relleno"}],
    "glossary": [],
    "episode_summary": "x",
}
# Invalid: t002 is not covered by any unit.
INVALID = {**RESPONSE, "units": [{"from": "t001", "to": "t001", "type": "relleno"}]}


def make(llm=None):
    llm = llm or FakeLLMProvider(RESPONSE)
    segments = MemorySegmentationRepository()
    return SegmentEpisode(llm, MemoryLLMInputRepository(LLM_INPUT), segments), llm, segments


def test_calls_the_llm_once_and_stores_the_validated_record():
    use_case, llm, segments = make()
    record = use_case.execute("vid", effort="medium")

    [request] = llm.requests
    assert request.system == SYSTEM_PROMPT
    assert request.prompt == LLM_INPUT.prompt
    assert request.suffix is None and request.effort == "medium"
    labels = request.schema["properties"]["speakers"]["items"]["properties"]["label"]
    assert labels["enum"] == ["SPEAKER_00", "SPEAKER_01"]

    assert segments.items["vid"] == record
    assert record["provider"] == "fake" and record["model"] == "fake-model"
    assert record["prompt_version"] == PROMPT_VERSION
    assert record["response"] == RESPONSE
    assert record["usage"]["cache_read_input_tokens"] == 5
    assert record["attempt"] == 1
    assert record["validation_errors"] == [] and record["segmenter"] == "llm"


def test_cached_record_skips_the_llm_unless_forced():
    use_case, llm, _ = make()
    first = use_case.execute("vid")
    assert use_case.execute("vid") == first
    assert len(llm.requests) == 1
    use_case.execute("vid", force=True)
    assert len(llm.requests) == 2


def test_cache_is_keyed_on_model():
    use_case, _, segments = make()
    use_case.execute("vid")
    other = FakeLLMProvider(RESPONSE, model="other-model")
    SegmentEpisode(other, MemoryLLMInputRepository(LLM_INPUT), segments).execute("vid")
    assert len(other.requests) == 1


def test_an_invalid_response_is_retried_once_with_its_errors():
    use_case, llm, segments = make(FakeLLMProvider([INVALID, RESPONSE]))
    record = use_case.execute("vid")

    first, retry = llm.requests
    assert first.suffix is None
    assert "- not covered by any unit: t002" in retry.suffix
    assert '"to": "t001"' in retry.suffix  # the previous response
    assert retry.prompt == LLM_INPUT.prompt  # cacheable prefix unchanged

    assert segments.items["vid"] == record
    assert record["response"] == RESPONSE and record["attempt"] == 2
    assert record["first_attempt_errors"] == ["not covered by any unit: t002"]
    assert record["validation_errors"] == [] and record["segmenter"] == "llm"


def test_failing_twice_falls_back_to_deterministic_ingestion_without_more_calls():
    use_case, llm, segments = make(FakeLLMProvider(INVALID))
    record = use_case.execute("vid")

    assert len(llm.requests) == 2
    assert segments.items["vid"] == record
    assert record["attempt"] == 2 and record["segmenter"] == "deterministic"
    assert record["validation_errors"] == ["not covered by any unit: t002"]
    assert record["first_attempt_errors"] == ["not covered by any unit: t002"]

    assert use_case.execute("vid") == record  # cached: the fallback is final
    assert len(llm.requests) == 2


def test_a_failed_retry_call_keeps_the_paid_first_attempt_for_the_next_run():
    use_case, _, segments = make(FakeLLMProvider([INVALID, LLMError("overloaded")]))
    with pytest.raises(LLMError):
        use_case.execute("vid")
    saved = segments.items["vid"]
    assert saved["attempt"] == 1 and saved["response"] == INVALID

    llm = FakeLLMProvider(RESPONSE)
    record = SegmentEpisode(llm, MemoryLLMInputRepository(LLM_INPUT), segments).execute("vid")
    [retry] = llm.requests  # only the retry: the paid first attempt is not repeated
    assert "- not covered by any unit: t002" in retry.suffix
    assert record["attempt"] == 2 and record["segmenter"] == "llm"


def test_a_cached_record_from_before_validation_gains_its_fields_without_a_call():
    use_case, llm, segments = make()
    use_case.execute("vid")
    legacy = dict(segments.items["vid"])
    del legacy["validation_errors"], legacy["segmenter"]
    segments.items["vid"] = legacy

    record = use_case.execute("vid")
    assert len(llm.requests) == 1
    assert segments.items["vid"] == record
    assert record["validation_errors"] == [] and record["segmenter"] == "llm"


def test_errors_propagate_as_domain_errors():
    use_case, _, segments = make(FakeLLMProvider(error="model refusal"))
    with pytest.raises(LLMError):
        use_case.execute("vid")
    assert segments.items == {}
    with pytest.raises(StorageError):
        use_case.execute("missing")
