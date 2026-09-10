#!/usr/bin/env python
"""
JSON de WhisperX -> guion en Markdown (formato entrevista de periodico).

Toma el .json que genera `video_to_text.py` (con diarizacion) y produce un
fichero con una fila por intervencion:

    **SPEAKER_00** — Bueno, Jordi, que tenemos que volver a la oficina.

    **SPEAKER_01** — No, que volvemos a nuestra oficina de toda la vida.

Uso:
    python json_to_script.py output/2vv4hHAvqnE.json
    python json_to_script.py output/2vv4hHAvqnE.json --timestamps
    python json_to_script.py output/2vv4hHAvqnE.json --names SPEAKER_00=Jordi,SPEAKER_01=Marc
    python json_to_script.py output/2vv4hHAvqnE.json --table --title "Entrevista a Theker"
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

UNKNOWN = "SPEAKER_?"


def hhmmss(seconds: float | None) -> str:
    if seconds is None:
        return "--:--:--"
    s = int(float(seconds))
    return f"{s // 3600:02d}:{(s % 3600) // 60:02d}:{s % 60:02d}"


def segment_speaker(seg: dict) -> str | None:
    """Speaker del segmento; si falta, el mayoritario entre sus palabras."""
    if seg.get("speaker"):
        return seg["speaker"]
    votes: dict[str, int] = {}
    for w in seg.get("words", []):
        spk = w.get("speaker")
        if spk:
            votes[spk] = votes.get(spk, 0) + 1
    return max(votes, key=votes.get) if votes else None


def build_turns_by_segment(segments: list[dict]) -> list[dict]:
    """Agrupa segmentos consecutivos del mismo interlocutor en un turno."""
    turns: list[dict] = []
    last_known = UNKNOWN
    for seg in segments:
        text = (seg.get("text") or "").strip()
        if not text:
            continue
        spk = segment_speaker(seg)
        # Un segmento sin speaker se atribuye a quien venia hablando.
        spk = spk or last_known
        last_known = spk
        start, end = seg.get("start"), seg.get("end")
        if turns and turns[-1]["speaker"] == spk:
            turns[-1]["text"] += " " + text
            turns[-1]["end"] = end
        else:
            turns.append({"speaker": spk, "text": text, "start": start, "end": end})
    return turns


def build_turns_by_word(segments: list[dict], min_words: int) -> list[dict] | None:
    """Turnos a nivel de palabra: un segmento de Whisper suele contener varias
    intervenciones (pregunta y respuesta), asi que cortar por segmento pierde
    el dialogo. Devuelve None si el JSON no trae speakers por palabra."""
    words = []
    last_known = None
    for seg in segments:
        seg_spk = segment_speaker(seg)
        for w in seg.get("words", []):
            text = (w.get("word") or "").strip()
            if not text:
                continue
            spk = w.get("speaker") or seg_spk or last_known
            if spk:
                last_known = spk
            words.append({"speaker": spk or UNKNOWN, "text": text,
                          "start": w.get("start"), "end": w.get("end")})
    if not words or all(w["speaker"] == UNKNOWN for w in words):
        return None

    # Palabras iniciales sin speaker: se atribuyen al primero que aparezca.
    first = next((w["speaker"] for w in words if w["speaker"] != UNKNOWN), UNKNOWN)
    for w in words:
        if w["speaker"] == UNKNOWN:
            w["speaker"] = first
        else:
            break

    runs = group_runs(words)
    runs = smooth_runs(runs, min_words)
    runs = snap_to_sentences(runs)
    return [
        {
            "speaker": r[0]["speaker"],
            "text": " ".join(w["text"] for w in r),
            "start": next((w["start"] for w in r if w.get("start") is not None), None),
            "end": next((w["end"] for w in reversed(r) if w.get("end") is not None), None),
        }
        for r in runs
    ]


def group_runs(words: list[dict]) -> list[list[dict]]:
    runs: list[list[dict]] = []
    for w in words:
        if runs and runs[-1][0]["speaker"] == w["speaker"]:
            runs[-1].append(w)
        else:
            runs.append([w])
    return runs


SENT_END = re.compile(r"[.!?…:;]+[\"')\]]*$")


def snap_to_sentences(runs: list[list[dict]], window: int = 3) -> list[list[dict]]:
    """El corte entre hablantes cae a menudo a mitad de frase ('Mucho' /
    'robot, mucho robot'). Si hay un final de frase a un par de palabras del
    corte, se mueve el limite ahi."""
    for i in range(len(runs) - 1):
        a, b = runs[i], runs[i + 1]
        if not a or not b or SENT_END.search(a[-1]["text"]):
            continue

        # Mover palabras del principio de B al final de A.
        fwd = next(
            (k for k in range(1, min(window, len(b) - 1) + 1)
             if SENT_END.search(b[k - 1]["text"])),
            None,
        )
        # Mover palabras del final de A al principio de B.
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


def smooth_runs(runs: list[list[dict]], min_words: int) -> list[list[dict]]:
    """La diarizacion salta de hablante en palabras sueltas. Las rachas de menos
    de `min_words` palabras se absorben en el vecino mas largo."""
    if min_words <= 1:
        return runs
    for _ in range(10):  # basta con unas pocas pasadas; corta por seguridad
        if len(runs) < 2:
            break
        changed = False
        for i, run in enumerate(runs):
            if len(run) >= min_words:
                continue
            prev_run = runs[i - 1] if i > 0 else None
            next_run = runs[i + 1] if i + 1 < len(runs) else None
            if next_run is None or (prev_run is not None
                                    and len(prev_run) >= len(next_run)):
                target = prev_run
            else:
                target = next_run
            if target is None:
                continue
            new_spk = target[0]["speaker"]
            for w in run:
                w["speaker"] = new_spk
            changed = True
        if not changed:
            break
        runs = group_runs([w for r in runs for w in r])
    return runs


def parse_names(raw: str | None) -> dict[str, str]:
    if not raw:
        return {}
    names = {}
    for pair in raw.split(","):
        if "=" in pair:
            k, v = pair.split("=", 1)
            names[k.strip()] = v.strip()
    return names


def render(turns: list[dict], names: dict, title: str, timestamps: bool,
           table: bool) -> str:
    def label(spk: str) -> str:
        return names.get(spk, spk)

    out = [f"# {title}", ""]
    speakers = sorted({t["speaker"] for t in turns})
    out.append(
        f"*{len(turns)} intervenciones · {len(speakers)} interlocutores: "
        + ", ".join(label(s) for s in speakers)
        + "*"
    )
    out.append("")

    if table:
        header = ["Tiempo", "Interlocutor", "Intervención"] if timestamps else \
                 ["Interlocutor", "Intervención"]
        out.append("| " + " | ".join(header) + " |")
        out.append("|" + "|".join(["---"] * len(header)) + "|")
        for t in turns:
            text = t["text"].replace("|", "\\|")
            row = [f"`{hhmmss(t['start'])}`"] if timestamps else []
            row += [f"**{label(t['speaker'])}**", text]
            out.append("| " + " | ".join(row) + " |")
    else:
        for t in turns:
            stamp = f"`{hhmmss(t['start'])}` " if timestamps else ""
            out.append(f"{stamp}**{label(t['speaker'])}** — {t['text']}")
            out.append("")

    return "\n".join(out).rstrip() + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Convierte el JSON de WhisperX en un guion Markdown por interlocutor."
    )
    ap.add_argument("json_path", help="fichero .json generado por video_to_text.py")
    ap.add_argument("-o", "--output", default=None, help="fichero de salida (.md)")
    ap.add_argument("--title", default=None, help="titulo del documento")
    ap.add_argument("--timestamps", action="store_true", help="anadir marca de tiempo")
    ap.add_argument("--table", action="store_true", help="salida como tabla Markdown")
    ap.add_argument("--names", default=None,
                    help="renombrar: SPEAKER_00=Jordi,SPEAKER_01=Marc")
    ap.add_argument("--by-segment", action="store_true",
                    help="cortar los turnos por segmento en vez de por palabra")
    ap.add_argument("--min-words", type=int, default=4,
                    help="turnos mas cortos se absorben en el vecino (anti-ruido)")
    args = ap.parse_args()

    src = Path(args.json_path)
    data = json.loads(src.read_text(encoding="utf-8"))
    segments = data["segments"] if isinstance(data, dict) else data

    turns = None
    if not args.by_segment:
        turns = build_turns_by_word(segments, args.min_words)
    if turns is None:
        turns = build_turns_by_segment(segments)
    if not turns:
        raise SystemExit("El JSON no contiene segmentos con texto.")
    if all(t["speaker"] == UNKNOWN for t in turns):
        print("AVISO: el JSON no tiene etiquetas de hablante. Vuelve a generarlo "
              "con `video_to_text.py ... --diarize` para separar interlocutores.")

    md = render(
        turns,
        parse_names(args.names),
        args.title or f"Transcripción — {src.stem}",
        args.timestamps,
        args.table,
    )

    out_path = Path(args.output) if args.output else src.with_suffix(".guion.md")
    out_path.write_text(md, encoding="utf-8")
    print(f"{len(turns)} intervenciones -> {out_path}")


if __name__ == "__main__":
    main()
