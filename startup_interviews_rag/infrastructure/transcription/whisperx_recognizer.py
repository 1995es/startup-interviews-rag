"""`SpeechRecognizer` on WhisperX: transcription, word alignment and, when
an HF token is available, pyannote diarization.

Diarization needs HF_TOKEN and accepted terms for
pyannote/speaker-diarization-3.1 on huggingface.co. Without it the audio is
still transcribed, but everything comes out as a single speaker.
"""

import logging
import os
from pathlib import Path

from startup_interviews_rag.application.ports.transcription import (
    SpeechRecognizer,
    TranscriptionOptions,
)
from startup_interviews_rag.domain.transcript import TranscriptSegment, Word

log = logging.getLogger(__name__)


def _register_cuda_dlls() -> None:
    """On Windows CTranslate2 needs the cuDNN/cuBLAS DLLs shipped inside
    torch/lib and the nvidia-* packages, which are not on the PATH. Must run
    before whisperx is imported."""
    if os.name != "nt":
        return
    import torch

    root = Path(torch.__file__).parent
    for d in [root / "lib", *(root.parent / "nvidia").glob("*/bin")]:
        if d.is_dir():
            os.add_dll_directory(str(d))
            os.environ["PATH"] = f"{d}{os.pathsep}{os.environ.get('PATH', '')}"


# At import time, before anything can import whisperx: keep it here, and keep
# the whisperx imports local to the methods below.
_register_cuda_dlls()


class WhisperXRecognizer(SpeechRecognizer):
    """GPU/CPU is auto-detected. If the model fails to load on the GPU it is
    retried on CPU/int8; without `hf_token` diarization is skipped with a
    warning instead of aborting."""

    def __init__(self, hf_token: str | None = None, batch_size: int = 16) -> None:
        self._hf_token = hf_token
        self._batch_size = batch_size

    def recognize(self, audio: Path, options: TranscriptionOptions) -> list[TranscriptSegment]:
        import torch
        import whisperx

        device = "cuda" if torch.cuda.is_available() else "cpu"
        compute_type = "float16" if device == "cuda" else "int8"
        waveform = whisperx.load_audio(str(audio))

        log.info(f"Transcribing '{audio.name}' with {options.model} on {device} ...")
        # whisperx.load_model imports whisperx.asr lazily. Importing it here, outside
        # the try, keeps an import error from passing for a GPU failure.
        import whisperx.asr  # noqa: F401

        try:
            model = whisperx.load_model(
                options.model, device, compute_type=compute_type, language=options.language
            )
        except Exception as exc:  # e.g. a GPU without float16 or missing cuDNN DLLs
            if device == "cpu":
                raise
            log.info(f"GPU load failed ({exc}). Falling back to CPU/int8 (slower) ...")
            device, compute_type = "cpu", "int8"
            model = whisperx.load_model(
                options.model, device, compute_type=compute_type, language=options.language
            )
        result = model.transcribe(waveform, batch_size=self._batch_size, language=options.language)

        log.info(f"Aligning words (language: {result['language']}) ...")
        model_a, metadata = whisperx.load_align_model(
            language_code=result["language"], device=device
        )
        result = whisperx.align(
            result["segments"], model_a, metadata, waveform, device, return_char_alignments=False
        )

        if self._hf_token:
            from whisperx.diarize import DiarizationPipeline

            log.info("Diarizing ...")
            kwargs = {
                k: v
                for k, v in (
                    ("min_speakers", options.min_speakers),
                    ("max_speakers", options.max_speakers),
                )
                if v
            }
            pipeline = DiarizationPipeline(token=self._hf_token, device=device)
            result = whisperx.assign_word_speakers(pipeline(waveform, **kwargs), result)
        else:
            log.warning("HF_TOKEN not set, skipping diarization (single speaker).")

        return [_segment(s) for s in result["segments"]]


def _segment(seg: dict) -> TranscriptSegment:
    return TranscriptSegment(
        text=seg.get("text") or "",
        speaker=seg.get("speaker"),
        start=seg.get("start"),
        end=seg.get("end"),
        words=[
            Word(
                text=w.get("word") or "",
                speaker=w.get("speaker"),
                start=w.get("start"),
                end=w.get("end"),
            )
            for w in seg.get("words", [])
        ],
    )
