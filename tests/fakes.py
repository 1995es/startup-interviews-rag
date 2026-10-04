"""In-memory adapters for the ports: what dependency injection buys in tests."""

from video_rag.application.ports.llm import (
    LLMError,
    LLMProvider,
    StructuredRequest,
    StructuredResponse,
    TokenUsage,
)
from video_rag.application.ports.repositories import LLMInputRepository, SegmentationRepository
from video_rag.domain.numbering import LLMInput


class FakeLLMProvider(LLMProvider):
    def __init__(
        self, data: dict | None = None, model: str = "fake-model", error: str | None = None
    ) -> None:
        self._data = data or {"speakers": [], "units": [], "glossary": [], "episode_summary": ""}
        self._model = model
        self._error = error
        self.requests: list[StructuredRequest] = []

    @property
    def name(self) -> str:
        return "fake"

    @property
    def model(self) -> str:
        return self._model

    def generate_structured(self, request: StructuredRequest) -> StructuredResponse:
        self.requests.append(request)
        if self._error:
            raise LLMError(self._error)
        return StructuredResponse(
            data=self._data,
            model=self._model,
            served_by=self._model,
            request_id="req_1",
            usage=TokenUsage(100, 20, 5, 0),
        )


class MemoryLLMInputRepository(LLMInputRepository):
    def __init__(self, *inputs: LLMInput) -> None:
        self.items = {i.video_id: i for i in inputs}

    def get(self, video_id: str) -> LLMInput | None:
        return self.items.get(video_id)

    def save(self, llm_input: LLMInput) -> str:
        self.items[llm_input.video_id] = llm_input
        return f"memory://{llm_input.video_id}"

    def list_ids(self) -> list[str]:
        return sorted(self.items)


class MemorySegmentationRepository(SegmentationRepository):
    def __init__(self) -> None:
        self.items: dict[str, dict] = {}

    def get(self, video_id: str) -> dict | None:
        return self.items.get(video_id)

    def save(self, video_id: str, record: dict) -> str:
        self.items[video_id] = record
        return f"memory://{video_id}"
