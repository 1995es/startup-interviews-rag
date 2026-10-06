from abc import ABC, abstractmethod
from pathlib import Path

from video_rag.domain.errors import VideoRagError


class AudioError(VideoRagError):
    pass


class AudioSource(ABC):
    """Video URL -> 16 kHz mono wav on disk."""

    @abstractmethod
    def fetch(self, url: str) -> Path:
        """Raises AudioError if the audio cannot be obtained."""
