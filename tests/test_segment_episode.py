import pytest

from fakes import FakeLLMProvider, MemoryLLMInputRepository, MemorySegmentationRepository
from video_rag.application.ports.llm import LLMError
from video_rag.application.ports.repositories import StorageError
from video_rag.application.use_cases.segment_episode import SegmentEpisode
from video_rag.domain.numbering import build_llm_input
from video_rag.domain.segmentation import PROMPT_VERSION, SYSTEM_PROMPT
from video_rag.domain.transcript import Turn
from video_rag.domain.video import VideoMeta

LLM_INPUT = build_llm_input(
    VideoMeta(id="vid"),
    [Turn("Hola.", "SPEAKER_01", 0, 1), Turn("Adiós.", "SPEAKER_00", 1, 2)],
    150,
)
RESPONSE = {
    "speakers": [],
    "units": [{"from": "t001", "to": "t002"}],
    "glossary": [],
    "episode_summary": "x",
}


def make(llm=None):
    llm = llm or FakeLLMProvider(RESPONSE)
    segments = MemorySegmentationRepository()
    return SegmentEpisode(llm, MemoryLLMInputRepository(LLM_INPUT), segments), llm, segments


def test_calls_the_llm_once_and_stores_the_record():
    use_case, llm, segments = make()
    record = use_case.execute("vid", effort="medium")

    [request] = llm.requests
    assert request.system == SYSTEM_PROMPT
    assert request.prompt == LLM_INPUT.prompt
    assert request.suffix is None and request.effort == "medium"
    labels = request.schema["properties"]["speakers"]["items"]["properties"]["label"]
    assert labels["enum"] == ["SPEAKER_00", "SPEAKER_01"]

    assert segments.items["vid"] is record
    assert record["provider"] == "fake" and record["model"] == "fake-model"
    assert record["prompt_version"] == PROMPT_VERSION
    assert record["response"] == RESPONSE
    assert record["usage"]["cache_read_input_tokens"] == 5


def test_cached_record_skips_the_llm_unless_forced():
    use_case, llm, _ = make()
    first = use_case.execute("vid")
    assert use_case.execute("vid") is first
    assert len(llm.requests) == 1
    use_case.execute("vid", force=True)
    assert len(llm.requests) == 2


def test_cache_is_keyed_on_model():
    use_case, _, segments = make()
    use_case.execute("vid")
    other = FakeLLMProvider(RESPONSE, model="other-model")
    SegmentEpisode(other, MemoryLLMInputRepository(LLM_INPUT), segments).execute("vid")
    assert len(other.requests) == 1


def test_retry_sends_errors_and_previous_response_as_suffix():
    use_case, llm, _ = make()
    use_case.execute("vid")
    record = use_case.execute("vid", errors=["t009 does not exist"])
    suffix = llm.requests[-1].suffix
    assert "- t009 does not exist" in suffix and '"episode_summary": "x"' in suffix
    assert llm.requests[-1].prompt == LLM_INPUT.prompt  # cacheable prefix unchanged
    assert record["attempt"] == 2


def test_errors_propagate_as_domain_errors():
    use_case, _, segments = make(FakeLLMProvider(error="model refusal"))
    with pytest.raises(LLMError):
        use_case.execute("vid")
    assert segments.items == {}
    with pytest.raises(StorageError):
        use_case.execute("missing")
