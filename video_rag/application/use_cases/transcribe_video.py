import logging
from dataclasses import dataclass

from video_rag.application.ports.audio import AudioSource
from video_rag.application.ports.repositories import TranscriptRepository
from video_rag.application.ports.transcription import (
    SpeechRecognizer,
    TranscriptionError,
    TranscriptionOptions,
)
from video_rag.domain.transcript import Turn
from video_rag.domain.turns import build_turns

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class TranscriptionResult:
    key: str
    turns: list[Turn]
    location: str


class TranscribeVideo:
    """URL or local file -> wav -> recognized segments -> speaker turns,
    stored under `key` (default: the audio file stem, i.e. the video id).

    Steps of `execute()`:

    1. `AudioSource.fetch` turns the source into a 16 kHz mono wav on disk
       (for a URL, the file is named after the video id).
    2. `SpeechRecognizer.recognize` returns segments with word timings and,
       when diarization is available, a speaker per word.
    3. `build_turns` regroups the words into speaker turns: it cuts at the
       word where the speaker changes, merges runs shorter than
       `options.min_words` into a neighbour and moves each cut to the nearest
       sentence end. Without word timings it keeps one turn per segment.
       Times are rounded to milliseconds.
    4. `TranscriptRepository.save` writes the turns under `key`, replacing
       any previous transcript with that key.

    It always transcribes: an existing transcript is never reused (callers
    that want that, like PrepareLLMInput, check the repository first).
    Raises AudioError if the audio cannot be obtained, and TranscriptionError
    if recognition fails or produces no text."""

    def __init__(
        self, audio: AudioSource, recognizer: SpeechRecognizer, transcripts: TranscriptRepository
    ) -> None:
        self._audio = audio
        self._recognizer = recognizer
        self._transcripts = transcripts

    def execute(
        self, source: str, options: TranscriptionOptions, key: str | None = None
    ) -> TranscriptionResult:
        audio_path = self._audio.fetch(source)
        segments = self._recognizer.recognize(audio_path, options)

        turns = [t.rounded() for t in build_turns(segments, options.min_words)]
        if not turns:
            raise TranscriptionError("the transcription produced no text.")

        key = key or audio_path.stem
        location = self._transcripts.save(key, turns)
        speakers = sorted({t.speaker for t in turns})
        log.info(
            f"{len(turns)} rows, {len(speakers)} speakers ({', '.join(speakers)}) -> {location}"
        )
        return TranscriptionResult(key, turns, location)
