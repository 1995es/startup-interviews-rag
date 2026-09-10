#!/usr/bin/env python
"""
JSON plano de `youtube_to_json.py` -> guion en Markdown (entrevista de periodico).

Entrada: la lista [{text, speaker, start, end}] que escribe el pipeline, ya
agrupada por turnos. Aqui solo se maqueta; el corte de turnos (por palabra,
suavizado y ajuste a final de frase) vive en `youtube_to_json.py`.

Salida, una fila por intervencion:

    `00:01:11` **SPEAKER_02** — Mas 140 de coeficiente intelectual.

Uso:
    python json_to_script.py output/2vv4hHAvqnE.json --timestamps
    python json_to_script.py output/2vv4hHAvqnE.json --names SPEAKER_00=Jordi,SPEAKER_01=Marc
    python json_to_script.py output/2vv4hHAvqnE.json --table --title "Tertulia de itnig"
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

UNKNOWN = "SPEAKER_?"


def hhmmss(seconds: float | None) -> str:
    if seconds is None:
        return "--:--:--"
    s = int(float(seconds))
    return f"{s // 3600:02d}:{(s % 3600) // 60:02d}:{s % 60:02d}"


def load_turns(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise SystemExit(
            f"{path}: se esperaba la lista [{{text, speaker, start, end}}] que "
            "genera youtube_to_json.py."
        )
    turns = [
        {
            "text": " ".join((t.get("text") or "").split()),
            "speaker": t.get("speaker") or UNKNOWN,
            "start": t.get("start"),
            "end": t.get("end"),
        }
        for t in data
    ]
    return [t for t in turns if t["text"]]


def parse_names(raw: str | None) -> dict[str, str]:
    """'SPEAKER_00=Jordi,SPEAKER_01=Marc' -> {'SPEAKER_00': 'Jordi', ...}"""
    names = {}
    for pair in (raw or "").split(","):
        if "=" in pair:
            k, v = pair.split("=", 1)
            names[k.strip()] = v.strip()
    return names


def render(turns: list[dict], names: dict, title: str, timestamps: bool,
           table: bool) -> str:
    def label(spk: str) -> str:
        return names.get(spk, spk)

    speakers = sorted({t["speaker"] for t in turns})
    out = [
        f"# {title}",
        "",
        f"*{len(turns)} intervenciones · {len(speakers)} interlocutores: "
        + ", ".join(label(s) for s in speakers)
        + "*",
        "",
    ]

    if table:
        header = ["Tiempo", "Interlocutor", "Intervención"] if timestamps else \
                 ["Interlocutor", "Intervención"]
        out.append("| " + " | ".join(header) + " |")
        out.append("|" + "|".join(["---"] * len(header)) + "|")
        for t in turns:
            row = [f"`{hhmmss(t['start'])}`"] if timestamps else []
            row += [f"**{label(t['speaker'])}**", t["text"].replace("|", "\\|")]
            out.append("| " + " | ".join(row) + " |")
    else:
        for t in turns:
            stamp = f"`{hhmmss(t['start'])}` " if timestamps else ""
            out.append(f"{stamp}**{label(t['speaker'])}** — {t['text']}")
            out.append("")

    return "\n".join(out).rstrip() + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Convierte el JSON plano del pipeline en un guion Markdown."
    )
    ap.add_argument("json_path", help="fichero .json generado por youtube_to_json.py")
    ap.add_argument("-o", "--output", default=None,
                    help="fichero de salida (por defecto <nombre>.guion.md)")
    ap.add_argument("--title", default=None, help="titulo del documento")
    ap.add_argument("--timestamps", action="store_true", help="anadir marca de tiempo")
    ap.add_argument("--table", action="store_true", help="salida como tabla Markdown")
    ap.add_argument("--names", default=None,
                    help="renombrar: SPEAKER_00=Jordi,SPEAKER_01=Marc")
    args = ap.parse_args()

    src = Path(args.json_path)
    turns = load_turns(src)
    if not turns:
        raise SystemExit(f"{src} no contiene intervenciones con texto.")
    if all(t["speaker"] == UNKNOWN for t in turns):
        print("AVISO: el JSON no trae etiquetas de hablante. Vuelve a generarlo "
              "con HF_TOKEN en el entorno para separar interlocutores.")

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
