"""In-memory adapters for the ports: what dependency injection buys in tests."""

from pathlib import Path

from startup_interviews_rag.application.ports.audio import AudioSource
from startup_interviews_rag.application.ports.llm import (
    LLMError,
    LLMProvider,
    StructuredRequest,
    StructuredResponse,
    TokenUsage,
)
from startup_interviews_rag.application.ports.metadata import VideoMetadataSource
from startup_interviews_rag.application.ports.repositories import (
    LLMInputRepository,
    MetadataRepository,
    SegmentationRepository,
    TranscriptRepository,
)
from startup_interviews_rag.application.ports.transcription import (
    SpeechRecognizer,
    TranscriptionOptions,
)
from startup_interviews_rag.domain.numbering import LLMInput
from startup_interviews_rag.domain.transcript import TranscriptSegment, Turn
from startup_interviews_rag.domain.video import VideoMeta, video_id


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


class FakeMetadataSource(VideoMetadataSource):
    def __init__(self) -> None:
        self.calls: list[str] = []

    def fetch(self, url: str) -> VideoMeta:
        self.calls.append(url)
        return VideoMeta(id=video_id(url) or "unknown", title="Fake title")


class MemoryMetadataRepository(MetadataRepository):
    def __init__(self, *metas: VideoMeta) -> None:
        self.items = {m.id: m for m in metas}

    def get(self, video_id: str) -> VideoMeta | None:
        return self.items.get(video_id)

    def save(self, meta: VideoMeta) -> str:
        self.items[meta.id] = meta
        return f"memory://{meta.id}"


class FakeAudioSource(AudioSource):
    def __init__(self) -> None:
        self.calls: list[str] = []

    def fetch(self, url: str) -> Path:
        self.calls.append(url)
        return Path(f"audio/{video_id(url)}.wav")


class FakeRecognizer(SpeechRecognizer):
    def __init__(self, segments: list[TranscriptSegment]) -> None:
        self._segments = segments
        self.calls: list[tuple[Path, TranscriptionOptions]] = []

    def recognize(self, audio: Path, options: TranscriptionOptions) -> list[TranscriptSegment]:
        self.calls.append((audio, options))
        return self._segments


class MemoryTranscriptRepository(TranscriptRepository):
    def __init__(self, **transcripts: list[Turn]) -> None:
        self.items = dict(transcripts)

    def get(self, key: str) -> list[Turn] | None:
        return self.items.get(key)

    def save(self, key: str, turns: list[Turn]) -> str:
        self.items[key] = turns
        return f"memory://{key}"
