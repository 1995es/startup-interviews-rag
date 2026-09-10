#!/usr/bin/env python
"""
Video -> Texto en un solo script (WhisperX, 100% local).

Version local del notebook `Demo_WhisperX.ipynb` (Colab). Cambios principales:
  * Sin dependencias de `google.colab` (ni `files.download` ni `userdata`):
    los ficheros se guardan en disco y el token de HuggingFace se lee de la
    variable de entorno HF_TOKEN (o de --hf-token).
  * Acepta una URL de YouTube *o* un fichero de video/audio local.
  * Detecta GPU/CPU automaticamente y cae a CPU/int8 si CUDA falla.
  * Arregla la carga de las DLL de cuDNN/cuBLAS en Windows para CTranslate2.

Pipeline:
    entrada (URL | fichero) -> audio wav 16 kHz mono -> transcripcion Whisper
    -> alineacion (timestamps por palabra) -> [diarizacion opcional]
    -> salidas .txt / .json / .srt

Uso:
    python video_to_text.py "https://www.youtube.com/watch?v=2vv4hHAvqnE"
    python video_to_text.py "C:/ruta/a/mi_video.mp4" --language es --model large-v2
    python video_to_text.py video.mp4 --diarize --min-speakers 2
"""

from __future__ import annotations

import argparse
import gc
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path


# --------------------------------------------------------------------------- #
# Windows: CTranslate2 (faster-whisper) necesita cuDNN/cuBLAS. Las DLL vienen
# dentro de torch/lib y de los paquetes nvidia-*, pero no estan en el PATH.
# Hay que registrarlas ANTES de importar whisperx.
# --------------------------------------------------------------------------- #
def _register_cuda_dlls() -> None:
    if os.name != "nt":
        return
    try:
        import torch  # noqa: F401
    except Exception:
        return

    candidates = []
    import torch as _torch

    candidates.append(Path(_torch.__file__).parent / "lib")

    site_packages = Path(_torch.__file__).parent.parent
    nvidia_dir = site_packages / "nvidia"
    if nvidia_dir.is_dir():
        candidates.extend(p for p in nvidia_dir.glob("*/bin") if p.is_dir())
        candidates.extend(p for p in nvidia_dir.glob("*/lib") if p.is_dir())

    for d in candidates:
        if d.is_dir():
            try:
                os.add_dll_directory(str(d))
            except OSError:
                pass
            os.environ["PATH"] = str(d) + os.pathsep + os.environ.get("PATH", "")


_register_cuda_dlls()


URL_RE = re.compile(r"^https?://", re.IGNORECASE)


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


# --------------------------------------------------------------------------- #
# 1. Entrada -> audio wav 16 kHz mono
# --------------------------------------------------------------------------- #
def _require_ffmpeg() -> None:
    if shutil.which("ffmpeg") is None:
        sys.exit(
            "ERROR: no se encuentra 'ffmpeg' en el PATH.\n"
            "Instalalo con:  winget install Gyan.FFmpeg   (Windows)\n"
            "                brew install ffmpeg          (macOS)\n"
            "                sudo apt install ffmpeg      (Linux)"
        )


def download_audio(url: str, out_dir: Path) -> Path:
    """Descarga el audio de una URL (YouTube, etc.) como wav 16 kHz mono."""
    import yt_dlp

    out_dir.mkdir(parents=True, exist_ok=True)

    def opts_for(fmt: str) -> dict:
        return {
            "format": fmt,
            "outtmpl": str(out_dir / "%(id)s.%(ext)s"),
            "postprocessors": [
                {"key": "FFmpegExtractAudio", "preferredcodec": "wav"}
            ],
            # 16 kHz mono, que es lo que espera Whisper
            "postprocessor_args": ["-ar", "16000", "-ac", "1"],
            "quiet": True,
            "no_warnings": True,
            "noprogress": True,
            "retries": 10,
            "fragment_retries": 10,
        }

    # YouTube devuelve a veces 403 en el formato "mejor audio" segun el cliente
    # que use yt-dlp; probamos varias cadenas de formato antes de rendirnos.
    last_err = None
    for fmt in ("bestaudio/best", "251/140/bestaudio", "18/best"):
        try:
            with yt_dlp.YoutubeDL(opts_for(fmt)) as ydl:
                info = ydl.extract_info(url, download=True)
            path = out_dir / f"{info['id']}.wav"
            if path.exists():
                log(f"Video: {info.get('title', '?')}  ({info.get('duration', 0)}s)")
                return path
            last_err = f"yt-dlp no genero {path}"
        except Exception as exc:
            last_err = exc
            log(f"Fallo con format='{fmt}' ({exc}). Reintentando ...")
    sys.exit(f"ERROR descargando el audio: {last_err}")


def extract_audio(video_path: Path, out_dir: Path) -> Path:
    """Extrae el audio de un fichero local con ffmpeg -> wav 16 kHz mono."""
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{video_path.stem}.wav"
    cmd = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le",
        str(out_path),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        sys.exit(f"ERROR de ffmpeg:\n{proc.stderr[-2000:]}")
    return out_path


def get_audio(source: str, out_dir: Path) -> Path:
    _require_ffmpeg()
    if URL_RE.match(source):
        log(f"Descargando audio de {source} ...")
        return download_audio(source, out_dir)

    path = Path(source).expanduser()
    if not path.exists():
        sys.exit(f"ERROR: no existe el fichero {path}")
    if path.suffix.lower() == ".wav":
        log(f"Usando el wav local {path}")
        return path
    log(f"Extrayendo audio de {path} ...")
    return extract_audio(path, out_dir)


# --------------------------------------------------------------------------- #
# 2. Dispositivo
# --------------------------------------------------------------------------- #
def pick_device(device: str, compute_type: str | None) -> tuple[str, str]:
    import torch

    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    if compute_type is None:
        compute_type = "float16" if device == "cuda" else "int8"
    if device == "cuda":
        log(f"GPU: {torch.cuda.get_device_name(0)}  (compute_type={compute_type})")
    else:
        log(f"CPU  (compute_type={compute_type}) - sera bastante mas lento")
    return device, compute_type


def free(*objs) -> None:
    for o in objs:
        del o
    gc.collect()
    try:
        import torch

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    except Exception:
        pass


# --------------------------------------------------------------------------- #
# 3. Transcripcion + alineacion + diarizacion
# --------------------------------------------------------------------------- #
def transcribe(audio, model_name, device, compute_type, batch_size, language):
    import whisperx

    log(f"Cargando modelo Whisper '{model_name}' ...")
    # Pasar `language` tambien aqui evita la fase de deteccion de idioma.
    try:
        model = whisperx.load_model(
            model_name, device, compute_type=compute_type, language=language
        )
    except Exception as exc:  # p.ej. GPU sin float16 o sin cuDNN
        if device != "cuda":
            raise
        log(f"Fallo cargando en GPU ({exc}). Reintentando en CPU/int8 ...")
        device, compute_type = "cpu", "int8"
        model = whisperx.load_model(
            model_name, device, compute_type=compute_type, language=language
        )

    log("Transcribiendo ...")
    result = model.transcribe(audio, batch_size=batch_size, language=language)
    free(model)
    return result, device


def align(result, audio, device):
    import whisperx

    log(f"Alineando timestamps (idioma detectado: {result['language']}) ...")
    model_a, metadata = whisperx.load_align_model(
        language_code=result["language"], device=device
    )
    aligned = whisperx.align(
        result["segments"], model_a, metadata, audio, device,
        return_char_alignments=False,
    )
    aligned["language"] = result["language"]
    free(model_a)
    return aligned


def diarize(result, audio, device, hf_token, min_speakers, max_speakers):
    import whisperx

    if not hf_token:
        log(
            "AVISO: diarizacion pedida pero no hay HF_TOKEN. "
            "Exporta HF_TOKEN o usa --hf-token, y acepta las condiciones de "
            "pyannote/speaker-diarization-3.1 en huggingface.co. Se omite."
        )
        return result, None

    from whisperx.diarize import DiarizationPipeline

    log("Diarizando (quien habla y cuando) ...")
    try:  # whisperx >= 3.4
        pipeline = DiarizationPipeline(token=hf_token, device=device)
    except TypeError:  # versiones anteriores
        pipeline = DiarizationPipeline(use_auth_token=hf_token, device=device)

    kwargs = {}
    if min_speakers:
        kwargs["min_speakers"] = min_speakers
    if max_speakers:
        kwargs["max_speakers"] = max_speakers

    diarize_segments = pipeline(audio, **kwargs)
    result = whisperx.assign_word_speakers(diarize_segments, result)
    free(pipeline)
    return result, diarize_segments


# --------------------------------------------------------------------------- #
# 4. Salidas
# --------------------------------------------------------------------------- #
def srt_time(seconds: float) -> str:
    ms = int(round(float(seconds) * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_outputs(result, out_dir: Path, stem: str, diarized: bool) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    segments = result["segments"]
    paths = {}

    # Texto plano
    txt = "\n".join(seg.get("text", "").strip() for seg in segments)
    p = out_dir / f"{stem}.txt"
    p.write_text(txt, encoding="utf-8")
    paths["txt"] = p

    # JSON completo con timestamps (y speakers si hubo diarizacion)
    p = out_dir / f"{stem}.json"
    p.write_text(
        json.dumps(result, indent=2, ensure_ascii=False, default=str),
        encoding="utf-8",
    )
    paths["json"] = p

    # SRT
    lines = []
    for i, seg in enumerate(segments, 1):
        start = seg.get("start", 0.0)
        end = seg.get("end", start)
        text = seg.get("text", "").strip()
        if diarized and seg.get("speaker"):
            text = f"[{seg['speaker']}] {text}"
        lines.append(f"{i}\n{srt_time(start)} --> {srt_time(end)}\n{text}\n")
    p = out_dir / f"{stem}.srt"
    p.write_text("\n".join(lines), encoding="utf-8")
    paths["srt"] = p

    # Transcripcion con hablantes, agrupada por turnos
    if diarized:
        turns, current = [], None
        for seg in segments:
            spk = seg.get("speaker", "SPEAKER_?")
            text = seg.get("text", "").strip()
            if current and current[0] == spk:
                current[1] += " " + text
            else:
                if current:
                    turns.append(current)
                current = [spk, text]
        if current:
            turns.append(current)
        p = out_dir / f"{stem}.speakers.txt"
        p.write_text(
            "\n\n".join(f"{spk}: {text}" for spk, text in turns), encoding="utf-8"
        )
        paths["speakers"] = p

    return paths


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main() -> None:
    ap = argparse.ArgumentParser(
        description="Pipeline Video -> Texto con WhisperX (local).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    ap.add_argument("source", help="URL (YouTube, etc.) o ruta a un video/audio local")
    ap.add_argument("--model", default="large-v2", help="modelo Whisper (tiny..large-v3)")
    ap.add_argument("--language", default=None, help="codigo de idioma, p.ej. es (auto si se omite)")
    ap.add_argument("--device", default="auto", choices=["auto", "cuda", "cpu"])
    ap.add_argument("--compute-type", default=None, help="float16 | int8 | float32")
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--outdir", default="output", help="carpeta de salida")
    ap.add_argument("--audio-dir", default="audio", help="carpeta para el wav intermedio")
    ap.add_argument("--no-align", action="store_true", help="saltar la alineacion por palabra")
    ap.add_argument("--diarize", action="store_true", help="identificar hablantes (necesita HF_TOKEN)")
    ap.add_argument("--min-speakers", type=int, default=None)
    ap.add_argument("--max-speakers", type=int, default=None)
    ap.add_argument("--hf-token", default=os.environ.get("HF_TOKEN"))
    args = ap.parse_args()

    t0 = time.time()
    audio_path = get_audio(args.source, Path(args.audio_dir))
    log(f"Audio listo: {audio_path}")

    device, compute_type = pick_device(args.device, args.compute_type)

    import whisperx

    audio = whisperx.load_audio(str(audio_path))

    result, device = transcribe(
        audio, args.model, device, compute_type, args.batch_size, args.language
    )
    log(f"{len(result['segments'])} segmentos transcritos.")

    if not args.no_align:
        result = align(result, audio, device)

    diarized = False
    if args.diarize:
        result, diarize_segments = diarize(
            result, audio, device, args.hf_token,
            args.min_speakers, args.max_speakers,
        )
        diarized = diarize_segments is not None

    paths = write_outputs(result, Path(args.outdir), audio_path.stem, diarized)

    log(f"Listo en {time.time() - t0:.1f}s. Ficheros generados:")
    for kind, p in paths.items():
        log(f"  {kind:9s} -> {p}")

    preview = "\n".join(s.get("text", "").strip() for s in result["segments"][:5])
    print("\n--- Primeras lineas ---")
    print(preview)


if __name__ == "__main__":
    main()
