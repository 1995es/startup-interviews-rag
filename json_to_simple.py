#!/usr/bin/env python
"""
JSON de WhisperX -> JSON simplificado con solo text / speaker / start / end.

    [
      {"text": "Bueno, Jordi, que tenemos que volver a...",
       "speaker": "SPEAKER_01", "start": 0.563, "end": 3.264},
      ...
    ]

Por defecto agrupa por turno de hablante con la misma logica que
`json_to_script.py` (corte por palabra + suavizado + ajuste a final de frase).

Uso:
    python json_to_simple.py output/2vv4hHAvqnE.json
    python json_to_simple.py output/2vv4hHAvqnE.json --by-segment
    python json_to_simple.py output/2vv4hHAvqnE.json --by-word -o palabras.json
    python json_to_simple.py output/2vv4hHAvqnE.json --names SPEAKER_00=Jordi
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from json_to_script import (
    UNKNOWN,
    build_turns_by_segment,
    build_turns_by_word,
    parse_names,
    segment_speaker,
)


def rounded(value, ndigits: int | None):
    if value is None or ndigits is None:
        return value
    return round(float(value), ndigits)


def rows_by_word(segments: list[dict]) -> list[dict]:
    """Una fila por palabra, conservando su speaker y sus tiempos."""
    rows = []
    last_known = UNKNOWN
    for seg in segments:
        seg_spk = segment_speaker(seg)
        for w in seg.get("words", []):
            text = (w.get("word") or "").strip()
            if not text:
                continue
            spk = w.get("speaker") or seg_spk or last_known
            last_known = spk
            rows.append({"text": text, "speaker": spk,
                         "start": w.get("start"), "end": w.get("end")})
    return rows


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Reduce el JSON de WhisperX a text/speaker/start/end."
    )
    ap.add_argument("json_path", help="fichero .json generado por video_to_text.py")
    ap.add_argument("-o", "--output", default=None,
                    help="fichero de salida (por defecto <nombre>.simple.json)")
    granularity = ap.add_mutually_exclusive_group()
    granularity.add_argument("--by-segment", action="store_true",
                             help="una fila por segmento de Whisper")
    granularity.add_argument("--by-word", action="store_true",
                             help="una fila por palabra")
    ap.add_argument("--min-words", type=int, default=4,
                    help="anti-ruido al agrupar por turnos (solo modo turno)")
    ap.add_argument("--names", default=None,
                    help="renombrar: SPEAKER_00=Jordi,SPEAKER_01=Marc")
    ap.add_argument("--round", type=int, default=3, dest="ndigits",
                    help="decimales de los tiempos (-1 para no redondear)")
    ap.add_argument("--indent", type=int, default=2, help="indentado del JSON")
    args = ap.parse_args()

    src = Path(args.json_path)
    data = json.loads(src.read_text(encoding="utf-8"))
    segments = data["segments"] if isinstance(data, dict) else data

    if args.by_word:
        rows = rows_by_word(segments)
    elif args.by_segment:
        rows = [
            {"text": t["text"], "speaker": t["speaker"],
             "start": t["start"], "end": t["end"]}
            for t in build_turns_by_segment(segments)
        ]
    else:
        turns = build_turns_by_word(segments, args.min_words)
        if turns is None:  # JSON sin diarizacion: no hay speakers por palabra
            turns = build_turns_by_segment(segments)
        rows = [
            {"text": t["text"], "speaker": t["speaker"],
             "start": t["start"], "end": t["end"]}
            for t in turns
        ]

    names = parse_names(args.names)
    ndigits = None if args.ndigits < 0 else args.ndigits
    rows = [
        {
            "text": r["text"].strip(),
            "speaker": names.get(r["speaker"], r["speaker"]),
            "start": rounded(r["start"], ndigits),
            "end": rounded(r["end"], ndigits),
        }
        for r in rows
        if r["text"].strip()
    ]

    out_path = Path(args.output) if args.output else src.with_suffix(".simple.json")
    out_path.write_text(
        json.dumps(rows, indent=args.indent, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    speakers = sorted({r["speaker"] for r in rows})
    print(f"{len(rows)} filas · {len(speakers)} hablantes ({', '.join(speakers)}) "
          f"-> {out_path}")


if __name__ == "__main__":
    main()
