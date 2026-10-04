import logging
from dataclasses import dataclass

from video_rag.application.ports.metadata import VideoMetadataSource
from video_rag.application.ports.repositories import (
    LLMInputRepository,
    MetadataRepository,
    TranscriptRepository,
)
from video_rag.application.ports.transcription import Transcriber, TranscriptionOptions
from video_rag.domain.numbering import DEFAULT_MAX_TURN_WORDS, LLMInput, build_llm_input
from video_rag.domain.video import VideoMeta, video_id

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class PreparedInput:
    llm_input: LLMInput
    turns: int
    location: str


class PrepareLLMInput:
    """Step 1 of docs/ingesta-llm.md: URL -> metadata + transcript ->
    numbered LLM input. Metadata and transcript are reused when already
    stored (no network, no speech models) unless `force` is set."""

    def __init__(
        self,
        metadata_source: VideoMetadataSource,
        metadata: MetadataRepository,
        transcriber: Transcriber,
        transcripts: TranscriptRepository,
        llm_inputs: LLMInputRepository,
    ) -> None:
        self._metadata_source = metadata_source
        self._metadata = metadata
        self._transcriber = transcriber
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
            turns = self._transcriber.transcribe(url, options)
            self._transcripts.save(meta.id, turns)

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
