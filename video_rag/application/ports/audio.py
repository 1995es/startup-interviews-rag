from abc import ABC, abstractmethod
from pathlib import Path

from video_rag.domain.errors import VideoRagError


class AudioError(VideoRagError):
    pass


class AudioSource(ABC):
    """URL or local video/audio file -> 16 kHz mono wav on disk."""

    @abstractmethod
    def fetch(self, source: str) -> Path:
        """Raises AudioError if the audio cannot be obtained."""
