"""WhisperXRecognizer against in-memory stand-ins for torch and whisperx."""

import sys
import types
from pathlib import Path

import pytest

from startup_interviews_rag.application.ports.transcription import TranscriptionOptions
from startup_interviews_rag.infrastructure.transcription.whisperx_recognizer import (
    WhisperXRecognizer,
)

AUDIO = Path("audio/yOLw6ncCJwY.wav")
WAVEFORM = object()  # what load_audio returns: must reach every model, not the path
SEGMENT = {
    "text": "Hola.",
    "start": 0.0,
    "end": 0.5,
    "words": [{"word": "Hola.", "start": 0.0, "end": 0.5, "speaker": "SPEAKER_01"}],
}


class FakeWhisperX:
    def __init__(self, gpu_load_fails: bool = False) -> None:
        self.gpu_load_fails = gpu_load_fails
        self.loads: list[str] = []
        self.inputs: list[object] = []

    def install(self, monkeypatch, cuda: bool = True) -> None:
        torch = types.ModuleType("torch")
        torch.cuda = types.SimpleNamespace(is_available=lambda: cuda)
        wx = types.ModuleType("whisperx")
        wx.load_audio = lambda path: WAVEFORM
        wx.load_model = self.load_model
        wx.load_align_model = lambda language_code, device: ("align", "meta")
        wx.align = self.align
        wx.assign_word_speakers = lambda diarization, result: result
        diarize = types.ModuleType("whisperx.diarize")
        diarize.DiarizationPipeline = lambda token, device: self.diarize
        monkeypatch.setitem(sys.modules, "torch", torch)
        monkeypatch.setitem(sys.modules, "whisperx", wx)
        monkeypatch.setitem(sys.modules, "whisperx.asr", types.ModuleType("whisperx.asr"))
        monkeypatch.setitem(sys.modules, "whisperx.diarize", diarize)

    def load_model(self, name, device, compute_type, language):
        self.loads.append(device)
        if device == "cuda" and self.gpu_load_fails:
            raise RuntimeError("no float16 on this GPU")
        return types.SimpleNamespace(transcribe=self.transcribe)

    def transcribe(self, audio, batch_size, language):
        self.inputs.append(audio)
        return {"language": "es", "segments": [SEGMENT]}

    def align(self, segments, model, metadata, audio, device, return_char_alignments):
        self.inputs.append(audio)
        return {"segments": segments}

    def diarize(self, audio, **kwargs):
        self.inputs.append(audio)
        return "diarization"


def test_recognize_feeds_the_waveform_to_every_model(monkeypatch):
    fake = FakeWhisperX()
    fake.install(monkeypatch)
    segments = WhisperXRecognizer(hf_token="hf").recognize(AUDIO, TranscriptionOptions())

    assert fake.inputs == [WAVEFORM, WAVEFORM, WAVEFORM]  # transcribe, align, diarize
    assert segments[0].text == "Hola."
    assert segments[0].words[0].speaker == "SPEAKER_01"


def test_without_hf_token_it_skips_diarization(monkeypatch):
    fake = FakeWhisperX()
    fake.install(monkeypatch)
    WhisperXRecognizer().recognize(AUDIO, TranscriptionOptions())
    assert fake.inputs == [WAVEFORM, WAVEFORM]


def test_gpu_load_failure_falls_back_to_cpu(monkeypatch):
    fake = FakeWhisperX(gpu_load_fails=True)
    fake.install(monkeypatch)
    WhisperXRecognizer().recognize(AUDIO, TranscriptionOptions())
    assert fake.loads == ["cuda", "cpu"]


def test_import_error_is_not_mistaken_for_a_gpu_failure(monkeypatch):
    fake = FakeWhisperX()
    fake.install(monkeypatch)
    monkeypatch.setitem(sys.modules, "whisperx.asr", None)  # makes the import raise

    with pytest.raises(ImportError):
        WhisperXRecognizer().recognize(AUDIO, TranscriptionOptions())
    assert fake.loads == []
