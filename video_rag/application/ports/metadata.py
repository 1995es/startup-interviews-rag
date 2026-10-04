from abc import ABC, abstractmethod

from video_rag.domain.video import VideoMeta


class VideoMetadataSource(ABC):
    """Video URL -> metadata (title, date, description...), no download."""

    @abstractmethod
    def fetch(self, url: str) -> VideoMeta: ...
