#!/usr/bin/env python
"""YouTube URL (or local file) -> JSON [{text, speaker, start, end}] with WhisperX.

    python youtube_to_json.py "https://www.youtube.com/watch?v=..." --language en

Speaker diarization needs HF_TOKEN in the environment and accepted terms for
pyannote/speaker-diarization-3.1 on huggingface.co. Without it the audio is
still transcribed, but everything comes out as a single speaker.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path


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


_register_cuda_dlls()

SENT_END = re.compile(r"[.!?…:;]+[\"')\]]*$")


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def require_ffmpeg() -> None:
    """yt-dlp, the local conversion and whisperx.load_audio all shell out to
    the ffmpeg CLI."""
    if shutil.which("ffmpeg") is None:
        sys.exit(
            "ERROR: 'ffmpeg' is not on the PATH.\n"
            "  winget install Gyan.FFmpeg   (Windows)\n"
            "  brew install ffmpeg          (macOS)\n"
            "  sudo apt install ffmpeg      (Linux)"
        )


def get_audio(source: str, audio_dir: Path) -> Path:
    """Download or extract the audio as a 16 kHz mono wav."""
    require_ffmpeg()
    if re.match(r"^https?://", source, re.IGNORECASE):
        import yt_dlp

        audio_dir.mkdir(parents=True, exist_ok=True)
        opts = {
            "outtmpl": str(audio_dir / "%(id)s.%(ext)s"),
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "wav"}],
            "postprocessor_args": ["-ar", "16000", "-ac", "1"],
            "quiet": True,
            "no_warnings": True,
            "noprogress": True,
        }
        # YouTube answers 403 on some format strings depending on the client,
        # so a few of them are tried before giving up.
        for fmt in ("bestaudio/best", "251/140/bestaudio", "18/best"):
            try:
                with yt_dlp.YoutubeDL({**opts, "format": fmt}) as ydl:
                    info = ydl.extract_info(source, download=True)
                path = audio_dir / f"{info['id']}.wav"
                if path.exists():
                    return path
            except Exception as exc:
                log(f"format='{fmt}' failed ({exc}). Retrying ...")
        sys.exit("ERROR: could not download the audio.")

    path = Path(source).expanduser()
    if not path.exists():
        sys.exit(f"ERROR: {path} does not exist")
    if path.suffix.lower() == ".wav":
        return path

    audio_dir.mkdir(parents=True, exist_ok=True)
    wav = audio_dir / f"{path.stem}.wav"
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(path), "-vn", "-ac", "1", "-ar", "16000", str(wav)],
        check=True,
        capture_output=True,
    )
    return wav


def group_runs(words: list[dict]) -> list[list[dict]]:
    runs: list[list[dict]] = []
    for w in words:
        if runs and runs[-1][0]["speaker"] == w["speaker"]:
            runs[-1].append(w)
        else:
            runs.append([w])
    return runs


def smooth_runs(runs: list[list[dict]], min_words: int) -> list[list[dict]]:
    """Diarization flips speaker on isolated words: runs shorter than
    `min_words` are absorbed into the longer neighbour."""
    for _ in range(10):
        if len(runs) < 2:
            break
        changed = False
        for i, run in enumerate(runs):
            if len(run) >= min_words:
                continue
            prev_run = runs[i - 1] if i > 0 else None
            next_run = runs[i + 1] if i + 1 < len(runs) else None
            if next_run is None or (prev_run and len(prev_run) >= len(next_run)):
                target = prev_run
            else:
                target = next_run
            if target is None:
                continue
            for w in run:
                w["speaker"] = target[0]["speaker"]
            changed = True
        if not changed:
            break
        runs = group_runs([w for r in runs for w in r])
    return runs


def snap_to_sentences(runs: list[list[dict]], window: int = 3) -> list[list[dict]]:
    """Speaker changes often land mid-sentence; move the boundary to the
    nearest sentence end within `window` words."""
    for i in range(len(runs) - 1):
        a, b = runs[i], runs[i + 1]
        if not a or not b or SENT_END.search(a[-1]["text"]):
            continue

        fwd = next(
            (k for k in range(1, min(window, len(b) - 1) + 1)
             if SENT_END.search(b[k - 1]["text"])),
            None,
        )
        bwd = next(
            (j for j in range(1, min(window, len(a) - 1) + 1)
             if SENT_END.search(a[len(a) - j - 1]["text"])),
            None,
        )

        if fwd is not None and (bwd is None or fwd <= bwd):
            moved, b[:] = b[:fwd], b[fwd:]
            for w in moved:
                w["speaker"] = a[0]["speaker"]
            a.extend(moved)
        elif bwd is not None:
            moved, a[:] = a[len(a) - bwd:], a[: len(a) - bwd]
            for w in moved:
                w["speaker"] = b[0]["speaker"]
            b[:0] = moved
    return [r for r in runs if r]


def build_turns(segments: list[dict], min_words: int) -> list[dict]:
    """Turns are cut per word, not per segment: a Whisper segment lasts ~20 s
    and usually holds both a question and its answer."""
    words = []
    speaker = None
    for seg in segments:
        for w in seg.get("words", []):
            text = (w.get("word") or "").strip()
            if not text:
                continue
            speaker = w.get("speaker") or seg.get("speaker") or speaker
            words.append({"speaker": speaker, "text": text,
                          "start": w.get("start"), "end": w.get("end")})

    if not words:  # no word-level timings: fall back to one row per segment
        return [{"text": (s.get("text") or "").strip(),
                 "speaker": s.get("speaker") or "SPEAKER_00",
                 "start": s.get("start"), "end": s.get("end")}
                for s in segments if (s.get("text") or "").strip()]

    # Leading words before the first diarized one belong to that same speaker.
    first = next((w["speaker"] for w in words if w["speaker"]), "SPEAKER_00")
    for w in words:
        w["speaker"] = w["speaker"] or first

    runs = snap_to_sentences(smooth_runs(group_runs(words), min_words))
    return [
        {
            "text": " ".join(w["text"] for w in r),
            "speaker": r[0]["speaker"],
            "start": next((w["start"] for w in r if w.get("start") is not None), None),
            "end": next((w["end"] for w in reversed(r) if w.get("end") is not None), None),
        }
        for r in runs
    ]


def main() -> None:
    ap = argparse.ArgumentParser(
        description="YouTube URL or local file -> JSON [{text, speaker, start, end}]"
    )
    ap.add_argument("source", help="URL or path to a local video/audio file")
    ap.add_argument("-o", "--output", help="output .json (default: output/<id>.json)")
    ap.add_argument("--model", default="large-v2", help="Whisper model (tiny..large-v3)")
    ap.add_argument("--language", help="language code, e.g. en (auto-detected if omitted)")
    ap.add_argument("--min-speakers", type=int)
    ap.add_argument("--max-speakers", type=int)
    ap.add_argument("--min-words", type=int, default=4,
                    help="shorter turns are merged into their neighbour")
    args = ap.parse_args()

    import torch
    import whisperx

    device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if device == "cuda" else "int8"

    audio_path = get_audio(args.source, Path("audio"))
    audio = whisperx.load_audio(str(audio_path))

    log(f"Transcribing '{audio_path.name}' with {args.model} on {device} ...")
    try:
        model = whisperx.load_model(args.model, device, compute_type=compute_type,
                                    language=args.language)
    except Exception as exc:  # e.g. a GPU without float16 or missing cuDNN DLLs
        if device == "cpu":
            raise
        log(f"GPU load failed ({exc}). Falling back to CPU/int8 (slower) ...")
        device, compute_type = "cpu", "int8"
        model = whisperx.load_model(args.model, device, compute_type=compute_type,
                                    language=args.language)
    result = model.transcribe(audio, batch_size=16, language=args.language)

    log(f"Aligning words (language: {result['language']}) ...")
    model_a, metadata = whisperx.load_align_model(language_code=result["language"],
                                                  device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device,
                            return_char_alignments=False)

    hf_token = os.environ.get("HF_TOKEN")
    if hf_token:
        from whisperx.diarize import DiarizationPipeline

        log("Diarizing ...")
        kwargs = {k: v for k, v in (("min_speakers", args.min_speakers),
                                    ("max_speakers", args.max_speakers)) if v}
        pipeline = DiarizationPipeline(token=hf_token, device=device)
        result = whisperx.assign_word_speakers(pipeline(audio, **kwargs), result)
    else:
        log("WARNING: HF_TOKEN not set, skipping diarization (single speaker).")

    rows = [
        {"text": r["text"], "speaker": r["speaker"],
         "start": None if r["start"] is None else round(r["start"], 3),
         "end": None if r["end"] is None else round(r["end"], 3)}
        for r in build_turns(result["segments"], args.min_words)
    ]
    if not rows:
        sys.exit("ERROR: the transcription produced no text.")

    out_path = Path(args.output) if args.output else Path("output") / f"{audio_path.stem}.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")

    speakers = sorted({r["speaker"] for r in rows})
    log(f"{len(rows)} rows, {len(speakers)} speakers ({', '.join(speakers)}) -> {out_path}")


if __name__ == "__main__":
    main()
