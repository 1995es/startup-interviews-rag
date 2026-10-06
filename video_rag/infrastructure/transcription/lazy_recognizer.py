from collections.abc import Callable
from pathlib import Path

from video_rag.application.ports.transcription import SpeechRecognizer, TranscriptionOptions
from video_rag.domain.transcript import TranscriptSegment


class LazyRecognizer(SpeechRecognizer):
    """Builds the real recognizer on the first `recognize()`. Importing the
    WhisperX adapter loads torch on Windows, so a run that reuses a stored
    transcript should never pay for it."""

    def __init__(self, factory: Callable[[], SpeechRecognizer]) -> None:
        self._factory = factory
        self._recognizer: SpeechRecognizer | None = None

    def recognize(self, audio: Path, options: TranscriptionOptions) -> list[TranscriptSegment]:
        if self._recognizer is None:
            self._recognizer = self._factory()
        return self._recognizer.recognize(audio, options)
