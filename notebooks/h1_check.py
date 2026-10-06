"""H1 check: does pyannote's exclusive diarization fix speaker attribution?

Transcribes and aligns once, diarizes once, then assigns word speakers with
both pyannote outputs (`speaker_diarization`, the one WhisperX uses, and
`exclusive_speaker_diarization`) and prints, for the [start, end] window:
the raw pyannote intervals, the words with their speaker and the resulting
turns. Both full transcripts are saved to output/ for a wider comparison.

    PYTHONPATH=. python notebooks/h1_check.py audio/yOLw6ncCJwY.wav 144 152

It is embedded in the Colab notebook built by build_h1_notebook.py.
"""

import copy
import json
import sys
from pathlib import Path

import pandas as pd
import torch
import whisperx
from whisperx.diarize import DiarizationPipeline

from startup_interviews_rag.config import Settings
from startup_interviews_rag.domain.turns import build_turns
from startup_interviews_rag.infrastructure.transcription.whisperx_recognizer import _segment


def to_df(annotation) -> pd.DataFrame:
    df = pd.DataFrame(
        annotation.itertracks(yield_label=True), columns=["segment", "label", "speaker"]
    )
    df["start"] = df["segment"].apply(lambda s: s.start)
    df["end"] = df["segment"].apply(lambda s: s.end)
    return df


def in_window(start, end, t0, t1) -> bool:
    return start is not None and end is not None and end >= t0 and start <= t1


def main() -> None:
    audio_path, t0, t1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    hf_token = Settings.from_env().hf_token
    if not hf_token:
        sys.exit("HF_TOKEN is not set.")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if device == "cuda" else "int8"
    audio = whisperx.load_audio(audio_path)

    print(f"Transcribing on {device} ...", flush=True)
    model = whisperx.load_model("large-v2", device, compute_type=compute_type, language="es")
    result = model.transcribe(audio, batch_size=16, language="es")
    del model
    print("Aligning ...", flush=True)
    model_a, metadata = whisperx.load_align_model(language_code="es", device=device)
    aligned = whisperx.align(
        result["segments"], model_a, metadata, audio, device, return_char_alignments=False
    )
    del model_a
    if device == "cuda":
        torch.cuda.empty_cache()

    print("Diarizing ...", flush=True)
    pipeline = DiarizationPipeline(token=hf_token, device=device)
    output = pipeline.model(
        {"waveform": torch.from_numpy(audio[None, :]), "sample_rate": 16000}, min_speakers=2
    )

    stem = Path(audio_path).stem
    variants = {
        "overlapping": output.speaker_diarization,
        "exclusive": output.exclusive_speaker_diarization,
    }
    for name, annotation in variants.items():
        df = to_df(annotation)
        print(f"\n=== {name}: pyannote intervals in [{t0}, {t1}] ===")
        for _, row in df.iterrows():
            if in_window(row["start"], row["end"], t0, t1):
                print(f"  {row['start']:8.3f} - {row['end']:8.3f}  {row['speaker']}")

        assigned = whisperx.assign_word_speakers(df, copy.deepcopy(aligned))
        segments = [_segment(s) for s in assigned["segments"]]

        print(f"--- {name}: words ---")
        for seg in segments:
            for w in seg.words:
                if in_window(w.start, w.end, t0, t1):
                    print(f"  {w.start:8.3f} {w.speaker}  {w.text}")

        turns = [t.rounded() for t in build_turns(segments, 4)]
        print(f"--- {name}: turns ({len(turns)} in the whole video) ---")
        for t in turns:
            if in_window(t.start, t.end, t0, t1):
                print(f"  {t.start:8.3f}-{t.end:8.3f} {t.speaker}: {t.text}")

        out = Path("output") / f"{stem}.{name}.json"
        out.parent.mkdir(exist_ok=True)
        out.write_text(
            json.dumps([t.to_dict() for t in turns], indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"  -> {out}")


if __name__ == "__main__":
    main()
