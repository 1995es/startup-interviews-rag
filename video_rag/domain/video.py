import re
from dataclasses import asdict, dataclass, fields
from typing import Self

META_FIELDS = ("id", "title", "upload_date", "description", "channel", "duration", "webpage_url")


@dataclass(frozen=True)
class VideoMeta:
    """The useful subset of `yt-dlp --dump-json`: meta/<id>.json."""

    id: str
    title: str | None = None
    upload_date: str | None = None
    description: str | None = None
    channel: str | None = None
    duration: float | None = None
    webpage_url: str | None = None
    published: str | None = None

    @classmethod
    def from_info(cls, info: dict) -> Self:
        """Builds it from a yt-dlp info dict; `published` is derived from
        `upload_date` (YYYYMMDD -> YYYY-MM-DD)."""
        values = {k: info.get(k) for k in META_FIELDS}
        d = values.get("upload_date") or ""
        published = f"{d[:4]}-{d[4:6]}-{d[6:]}" if len(d) == 8 else None
        return cls(**values, published=published)

    @classmethod
    def from_dict(cls, data: dict) -> Self:
        return cls(**{f.name: data.get(f.name) for f in fields(cls)})

    def to_dict(self) -> dict:
        return asdict(self)


def video_id(url: str) -> str | None:
    """YouTube ID from watch?v=, youtu.be/, shorts/ or embed/ URLs, without
    touching the network."""
    m = re.search(r"(?:[?&]v=|youtu\.be/|/shorts/|/embed/)([\w-]{11})", url)
    return m.group(1) if m else None
