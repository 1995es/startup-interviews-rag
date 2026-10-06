from abc import ABC, abstractmethod

from startup_interviews_rag.domain.video import VideoMeta


class VideoMetadataSource(ABC):
    """Video URL -> metadata (title, date, description...), no download."""

    @abstractmethod
    def fetch(self, url: str) -> VideoMeta: ...
