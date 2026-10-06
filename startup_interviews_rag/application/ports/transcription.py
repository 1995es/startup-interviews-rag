from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from startup_interviews_rag.domain.errors import StartupInterviewsRagError
from startup_interviews_rag.domain.transcript import TranscriptSegment


class TranscriptionError(StartupInterviewsRagError):
    pass


@dataclass(frozen=True)
class TranscriptionOptions:
    model: str = "large-v2"
    language: str | None = None  # auto-detected if None
    min_speakers: int | None = None
    max_speakers: int | None = None
    min_words: int = 4  # shorter turns are merged into a neighbour


class SpeechRecognizer(ABC):
    """wav -> segments with word timings and, when diarization is available,
    word-level speakers."""

    @abstractmethod
    def recognize(self, audio: Path, options: TranscriptionOptions) -> list[TranscriptSegment]: ...
