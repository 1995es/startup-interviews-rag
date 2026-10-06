"""File-system repositories: one JSON file per video in a folder."""

import json
from pathlib import Path

from video_rag.application.ports.repositories import (
    LLMInputRepository,
    MetadataRepository,
    SegmentationRepository,
    StorageError,
    TranscriptRepository,
)
from video_rag.domain.numbering import IdUnit, LLMInput
from video_rag.domain.transcript import Turn
from video_rag.domain.video import VideoMeta


def _read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as exc:
        raise StorageError(f"{path} is not valid JSON: {exc}") from exc


def _write_json(path: Path, data) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return str(path)


class JsonTranscriptRepository(TranscriptRepository):
    """<dir>/<key>.json holding the flat list [{text, speaker, start, end}]."""

    def __init__(self, directory: Path) -> None:
        self._dir = directory

    def get(self, key: str) -> list[Turn] | None:
        path = self._dir / f"{key}.json"
        data = _read_json(path)
        if data is None:
            return None
        if not isinstance(data, list):
            raise StorageError(
                f"{path}: expected the list [{{text, speaker, start, end}}] written by prepare.py."
            )
        return [Turn.from_dict(row) for row in data]

    def save(self, key: str, turns: list[Turn]) -> str:
        return _write_json(self._dir / f"{key}.json", [t.to_dict() for t in turns])


class JsonMetadataRepository(MetadataRepository):
    def __init__(self, directory: Path) -> None:
        self._dir = directory

    def get(self, video_id: str) -> VideoMeta | None:
        data = _read_json(self._dir / f"{video_id}.json")
        return None if data is None else VideoMeta.from_dict(data)

    def save(self, meta: VideoMeta) -> str:
        return _write_json(self._dir / f"{meta.id}.json", meta.to_dict())


class FileLLMInputRepository(LLMInputRepository):
    """<id>.txt is the prompt as sent; <id>.json has the meta and every
    cuttable ID with its original text."""

    def __init__(self, directory: Path) -> None:
        self._dir = directory

    def get(self, video_id: str) -> LLMInput | None:
        data = _read_json(self._dir / f"{video_id}.json")
        if data is None:
            return None
        try:
            prompt = (self._dir / f"{video_id}.txt").read_text(encoding="utf-8")
        except FileNotFoundError:
            return None
        return LLMInput(
            video_id=data["video_id"],
            meta=VideoMeta.from_dict(data["meta"]),
            prompt=prompt,
            units=[IdUnit.from_dict(u) for u in data["units"]],
        )

    def save(self, llm_input: LLMInput) -> str:
        self._dir.mkdir(parents=True, exist_ok=True)
        txt = self._dir / f"{llm_input.video_id}.txt"
        txt.write_text(llm_input.prompt, encoding="utf-8")
        _write_json(
            self._dir / f"{llm_input.video_id}.json",
            {
                "video_id": llm_input.video_id,
                "meta": llm_input.meta.to_dict(),
                "units": [u.to_dict() for u in llm_input.units],
            },
        )
        return str(txt)

    def list_ids(self) -> list[str]:
        return sorted(p.stem for p in self._dir.glob("*.txt"))


class JsonSegmentationRepository(SegmentationRepository):
    def __init__(self, directory: Path) -> None:
        self._dir = directory

    def get(self, video_id: str) -> dict | None:
        return _read_json(self._dir / f"{video_id}.json")

    def save(self, video_id: str, record: dict) -> str:
        return _write_json(self._dir / f"{video_id}.json", record)
