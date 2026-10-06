import logging
from dataclasses import dataclass

from startup_interviews_rag.application.ports.audio import AudioSource
from startup_interviews_rag.application.ports.metadata import VideoMetadataSource
from startup_interviews_rag.application.ports.repositories import (
    LLMInputRepository,
    MetadataRepository,
    TranscriptRepository,
)
from startup_interviews_rag.application.ports.transcription import (
    SpeechRecognizer,
    TranscriptionError,
    TranscriptionOptions,
)
from startup_interviews_rag.domain.numbering import (
    DEFAULT_MAX_TURN_WORDS,
    LLMInput,
    build_llm_input,
)
from startup_interviews_rag.domain.transcript import Turn
from startup_interviews_rag.domain.turns import build_turns
from startup_interviews_rag.domain.video import VideoMeta, video_id

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class PreparedInput:
    llm_input: LLMInput
    turns: int
    location: str


class PrepareLLMInput:
    """Step 1 of docs/llm-ingestion.md: video URL -> metadata + transcript ->
    numbered LLM input.

    Steps of `execute()`:

    1. Metadata: `MetadataRepository` (meta/<id>.json) or, if missing,
       `VideoMetadataSource.fetch` without downloading the video.
    2. Transcript: `TranscriptRepository` (output/<id>.json) or, if missing:
       a. `AudioSource.fetch` turns the URL into a 16 kHz mono wav on disk.
       b. `SpeechRecognizer.recognize` returns segments with word timings
          and, when diarization is available, a speaker per word.
       c. `build_turns` regroups the words into speaker turns: it cuts at the
          word where the speaker changes, merges runs shorter than
          `options.min_words` into a neighbour and moves each cut to the
          nearest sentence end. Without word timings it keeps one turn per
          segment. Times are rounded to milliseconds.
       d. The turns are saved under the video id.
    3. `build_llm_input` numbers turns and sentences into llm_input/<id>.

    Stored metadata and transcript are reused (no network, no speech models)
    unless `force` is set. Raises AudioError if the audio cannot be obtained,
    and TranscriptionError if recognition fails or produces no text."""

    def __init__(
        self,
        metadata_source: VideoMetadataSource,
        metadata: MetadataRepository,
        audio: AudioSource,
        recognizer: SpeechRecognizer,
        transcripts: TranscriptRepository,
        llm_inputs: LLMInputRepository,
    ) -> None:
        self._metadata_source = metadata_source
        self._metadata = metadata
        self._audio = audio
        self._recognizer = recognizer
        self._transcripts = transcripts
        self._llm_inputs = llm_inputs

    def execute(
        self,
        url: str,
        options: TranscriptionOptions,
        max_turn_words: int = DEFAULT_MAX_TURN_WORDS,
        force: bool = False,
    ) -> PreparedInput:
        meta = self._meta(url, force)

        turns = None if force else self._transcripts.get(meta.id)
        if turns is not None:
            log.info(f"Reusing transcript {meta.id} (--force to redo it)")
        else:
            turns = self._transcribe(url, meta.id, options)

        llm_input = build_llm_input(meta, turns, max_turn_words)
        location = self._llm_inputs.save(llm_input)
        log.info(
            f"{len(turns)} turns ({llm_input.split_turns} split into sentences), "
            f"{len(llm_input.units)} IDs, ~{len(llm_input.prompt) // 4} tokens "
            f"-> {location}"
        )
        return PreparedInput(llm_input, len(turns), location)

    def _meta(self, url: str, force: bool) -> VideoMeta:
        vid = video_id(url)
        meta = self._metadata.get(vid) if vid and not force else None
        if meta is not None:
            log.info(f"Reusing metadata {vid} (--force to redo it)")
            return meta
        log.info("Fetching video metadata ...")
        meta = self._metadata_source.fetch(url)
        self._metadata.save(meta)
        return meta

    def _transcribe(self, url: str, key: str, options: TranscriptionOptions) -> list[Turn]:
        audio_path = self._audio.fetch(url)
        segments = self._recognizer.recognize(audio_path, options)

        turns = [t.rounded() for t in build_turns(segments, options.min_words)]
        if not turns:
            raise TranscriptionError("the transcription produced no text.")

        location = self._transcripts.save(key, turns)
        speakers = sorted({t.speaker for t in turns})
        log.info(
            f"{len(turns)} rows, {len(speakers)} speakers ({', '.join(speakers)}) -> {location}"
        )
        return turns
