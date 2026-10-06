import pytest

from fakes import (
    FakeAudioSource,
    FakeMetadataSource,
    FakeRecognizer,
    MemoryLLMInputRepository,
    MemoryMetadataRepository,
    MemoryTranscriptRepository,
)
from video_rag.application.ports.transcription import TranscriptionError, TranscriptionOptions
from video_rag.application.use_cases.prepare_llm_input import PrepareLLMInput
from video_rag.domain.transcript import TranscriptSegment, Turn, Word
from video_rag.domain.video import VideoMeta
from video_rag.infrastructure.transcription.lazy_recognizer import LazyRecognizer

URL = "https://www.youtube.com/watch?v=yOLw6ncCJwY"
VID = "yOLw6ncCJwY"
OPTIONS = TranscriptionOptions(min_words=1)
SEGMENT = TranscriptSegment(
    text="",
    words=[
        Word("Hola.", "SPEAKER_00", 0.0, 0.5),
        Word("Buenas", "SPEAKER_01", 1.0, 1.5),
        Word("tardes.", "SPEAKER_01", 1.5, 2.0001),
    ],
)


def make(segments=(SEGMENT,), metas=(), **transcripts):
    deps = {
        "metadata_source": FakeMetadataSource(),
        "metadata": MemoryMetadataRepository(*metas),
        "audio": FakeAudioSource(),
        "recognizer": FakeRecognizer(list(segments)),
        "transcripts": MemoryTranscriptRepository(**transcripts),
        "llm_inputs": MemoryLLMInputRepository(),
    }
    return PrepareLLMInput(**deps), deps


def test_transcribes_and_numbers_a_new_video():
    use_case, d = make()
    result = use_case.execute(URL, OPTIONS)

    assert d["metadata_source"].calls == [URL] and VID in d["metadata"].items
    assert d["audio"].calls == [URL]
    assert d["recognizer"].calls[0][0].name == f"{VID}.wav"
    assert d["transcripts"].items[VID] == [
        Turn("Hola.", "SPEAKER_00", 0.0, 0.5),
        Turn("Buenas tardes.", "SPEAKER_01", 1.0, 2.0),  # rounded to ms
    ]
    assert result.turns == 2
    assert result.llm_input.prompt.endswith(
        "[t001 00:00:00 SPEAKER_00] Hola.\n[t002 00:00:01 SPEAKER_01] Buenas tardes.\n"
    )
    assert d["llm_inputs"].get(VID) is result.llm_input


def test_stored_metadata_and_transcript_skip_network_and_speech_models():
    stored = [Turn("Ya estaba.", "SPEAKER_00", 0, 1)]
    use_case, d = make(metas=[VideoMeta(id=VID, title="T")], **{VID: stored})
    result = use_case.execute(URL, OPTIONS)

    assert d["metadata_source"].calls == []
    assert d["audio"].calls == [] and d["recognizer"].calls == []
    assert result.turns == 1


def test_force_redoes_metadata_and_transcript():
    stored = [Turn("Viejo.", "SPEAKER_00", 0, 1)]
    use_case, d = make(metas=[VideoMeta(id=VID)], **{VID: stored})
    use_case.execute(URL, OPTIONS, force=True)

    assert d["metadata_source"].calls == [URL]
    assert len(d["recognizer"].calls) == 1
    assert d["transcripts"].items[VID][0].text == "Hola."


def test_empty_transcription_raises():
    use_case, d = make(segments=[])
    with pytest.raises(TranscriptionError):
        use_case.execute(URL, OPTIONS)
    assert VID not in d["transcripts"].items


def test_lazy_recognizer_builds_the_real_one_on_first_use_only():
    built = []

    def factory():
        built.append(1)
        return FakeRecognizer([SEGMENT])

    lazy = LazyRecognizer(factory)
    assert built == []
    lazy.recognize(None, OPTIONS)
    lazy.recognize(None, OPTIONS)
    assert built == [1]
