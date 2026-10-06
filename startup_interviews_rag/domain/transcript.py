"""Transcript entities: what speech recognition produces (segments with
word-level timings) and what the pipeline stores (speaker turns)."""

from dataclasses import asdict, dataclass, field, replace
from typing import Self

# Label for speech that diarization did not attribute to anyone.
DEFAULT_SPEAKER = "SPEAKER_00"


@dataclass
class Word:
    """Mutable on purpose: turn building reassigns `speaker` in place."""

    text: str
    speaker: str | None = None
    start: float | None = None
    end: float | None = None


@dataclass(frozen=True)
class TranscriptSegment:
    """A recognizer segment (~20 s). `words` is empty when there are no
    word-level timings."""

    text: str
    speaker: str | None = None
    start: float | None = None
    end: float | None = None
    words: list[Word] = field(default_factory=list)


@dataclass(frozen=True)
class Turn:
    """One speaking turn: the row of output/<id>.json."""

    text: str
    speaker: str | None
    start: float | None
    end: float | None

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(
            text=data.get("text") or "",
            speaker=data.get("speaker"),
            start=data.get("start"),
            end=data.get("end"),
        )

    def to_dict(self) -> dict:
        return asdict(self)

    def rounded(self, ndigits: int = 3) -> Self:
        return replace(
            self,
            start=None if self.start is None else round(self.start, ndigits),
            end=None if self.end is None else round(self.end, ndigits),
        )
