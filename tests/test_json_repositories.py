import pytest

from video_rag.application.ports.repositories import StorageError
from video_rag.domain.numbering import build_llm_input
from video_rag.domain.transcript import Turn
from video_rag.domain.video import VideoMeta
from video_rag.infrastructure.persistence.json_repositories import (
    FileLLMInputRepository,
    JsonMetadataRepository,
    JsonSegmentationRepository,
    JsonTranscriptRepository,
)

TURNS = [Turn("Hola, ¿qué tal?", "SPEAKER_00", 0.0, 1.5), Turn("Bien.", None, 1.5, 2.0)]
META = VideoMeta(id="vid", title="Título", upload_date="20200107", published="2020-01-07")


def test_transcript_round_trip_keeps_non_ascii_text(tmp_path):
    repo = JsonTranscriptRepository(tmp_path / "output")
    assert repo.get("vid") is None
    repo.save("vid", TURNS)
    assert repo.get("vid") == TURNS
    assert "¿qué tal?" in (tmp_path / "output/vid.json").read_text(encoding="utf-8")


def test_transcript_with_the_wrong_shape_raises(tmp_path):
    (tmp_path / "vid.json").write_text('{"text": "x"}', encoding="utf-8")
    with pytest.raises(StorageError):
        JsonTranscriptRepository(tmp_path).get("vid")


def test_invalid_json_raises_storage_error(tmp_path):
    (tmp_path / "vid.json").write_text("{not json", encoding="utf-8")
    with pytest.raises(StorageError):
        JsonMetadataRepository(tmp_path).get("vid")


def test_metadata_round_trip(tmp_path):
    repo = JsonMetadataRepository(tmp_path)
    repo.save(META)
    assert repo.get("vid") == META


def test_llm_input_round_trip(tmp_path):
    repo = FileLLMInputRepository(tmp_path)
    llm_input = build_llm_input(META, TURNS, 150)
    repo.save(llm_input)
    assert repo.get("vid") == llm_input
    assert repo.list_ids() == ["vid"]


def test_llm_input_without_its_txt_is_missing(tmp_path):
    repo = FileLLMInputRepository(tmp_path)
    repo.save(build_llm_input(META, TURNS, 150))
    (tmp_path / "vid.txt").unlink()
    assert repo.get("vid") is None


def test_segmentation_round_trip(tmp_path):
    repo = JsonSegmentationRepository(tmp_path)
    record = {"video_id": "vid", "response": {"units": []}}
    repo.save("vid", record)
    assert repo.get("vid") == record
