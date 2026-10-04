"""Speaker turns -> Markdown script, newspaper-interview style. Layout only:
turns arrive already cut by the transcription pipeline.

    `00:01:11` **SPEAKER_02** — Over 140 IQ.
"""

from dataclasses import dataclass, field

from video_rag.domain.timecode import hhmmss
from video_rag.domain.transcript import Turn

UNKNOWN_SPEAKER = "SPEAKER_?"


@dataclass(frozen=True)
class ScriptOptions:
    title: str
    timestamps: bool = False
    table: bool = False
    names: dict[str, str] = field(default_factory=dict)


def clean_turns(turns: list[Turn]) -> list[Turn]:
    """Collapses whitespace, labels speakerless turns and drops empty ones."""
    cleaned = [
        Turn(" ".join((t.text or "").split()), t.speaker or UNKNOWN_SPEAKER, t.start, t.end)
        for t in turns
    ]
    return [t for t in cleaned if t.text]


def render_script(turns: list[Turn], options: ScriptOptions) -> str:
    def label(spk: str) -> str:
        return options.names.get(spk, spk)

    speakers = sorted({t.speaker for t in turns})
    out = [
        f"# {options.title}",
        "",
        f"*{len(turns)} turns · {len(speakers)} speakers: "
        + ", ".join(label(s) for s in speakers)
        + "*",
        "",
    ]

    if options.table:
        header = ["Time", "Speaker", "Text"] if options.timestamps else ["Speaker", "Text"]
        out.append("| " + " | ".join(header) + " |")
        out.append("|" + "|".join(["---"] * len(header)) + "|")
        for t in turns:
            row = [f"`{hhmmss(t.start)}`"] if options.timestamps else []
            row += [f"**{label(t.speaker)}**", t.text.replace("|", "\\|")]
            out.append("| " + " | ".join(row) + " |")
    else:
        for t in turns:
            stamp = f"`{hhmmss(t.start)}` " if options.timestamps else ""
            out.append(f"{stamp}**{label(t.speaker)}** — {t.text}")
            out.append("")

    return "\n".join(out).rstrip() + "\n"
