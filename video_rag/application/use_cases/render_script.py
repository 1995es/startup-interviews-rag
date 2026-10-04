from dataclasses import dataclass

from video_rag.application.ports.repositories import StorageError, TranscriptRepository
from video_rag.domain.script import UNKNOWN_SPEAKER, ScriptOptions, clean_turns, render_script


@dataclass(frozen=True)
class RenderedScript:
    markdown: str
    turns: int
    has_speakers: bool  # False when the transcript was not diarized


class RenderScript:
    """Stored transcript -> Markdown script. Writing it out is up to the
    caller (a file for the CLI, a response body for an API)."""

    def __init__(self, transcripts: TranscriptRepository) -> None:
        self._transcripts = transcripts

    def execute(self, key: str, options: ScriptOptions) -> RenderedScript:
        stored = self._transcripts.get(key)
        if stored is None:
            raise StorageError(f"transcript '{key}' not found.")
        turns = clean_turns(stored)
        if not turns:
            raise StorageError(f"transcript '{key}' has no turns with text.")
        return RenderedScript(
            markdown=render_script(turns, options),
            turns=len(turns),
            has_speakers=any(t.speaker != UNKNOWN_SPEAKER for t in turns),
        )
