"""Storage ports, one per pipeline artefact. Every `save` returns where the
artefact ended up, for logging."""

from abc import ABC, abstractmethod

from video_rag.domain.errors import VideoRagError
from video_rag.domain.numbering import LLMInput
from video_rag.domain.transcript import Turn
from video_rag.domain.video import VideoMeta


class StorageError(VideoRagError):
    pass


class TranscriptRepository(ABC):
    """Speaker turns of one video (output/<id>.json)."""

    @abstractmethod
    def get(self, key: str) -> list[Turn] | None: ...

    @abstractmethod
    def save(self, key: str, turns: list[Turn]) -> str: ...


class MetadataRepository(ABC):
    """Video metadata (meta/<id>.json)."""

    @abstractmethod
    def get(self, video_id: str) -> VideoMeta | None: ...

    @abstractmethod
    def save(self, meta: VideoMeta) -> str: ...


class LLMInputRepository(ABC):
    """Numbered transcript for the segmenter (llm_input/<id>.txt + .json)."""

    @abstractmethod
    def get(self, video_id: str) -> LLMInput | None: ...

    @abstractmethod
    def save(self, llm_input: LLMInput) -> str: ...

    @abstractmethod
    def list_ids(self) -> list[str]: ...


class SegmentationRepository(ABC):
    """LLM segmentation records with their cache metadata (segments/<id>.json)."""

    @abstractmethod
    def get(self, video_id: str) -> dict | None: ...

    @abstractmethod
    def save(self, video_id: str, record: dict) -> str: ...
