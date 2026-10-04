import json
import subprocess
import sys
import tempfile
from pathlib import Path

from video_rag.application.ports.transcription import (
    Transcriber,
    TranscriptionError,
    TranscriptionOptions,
)
from video_rag.domain.transcript import Turn

CLI_MODULE = "video_rag.interfaces.cli.transcribe"


class SubprocessTranscriber(Transcriber):
    """Runs the transcribe CLI in its own process: WhisperX/torch are never
    loaded in the caller, and a native crash (CTranslate2 segfault) shows up
    as an exit code instead of taking the caller down."""

    def transcribe(self, source: str, options: TranscriptionOptions) -> list[Turn]:
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "transcript.json"
            cmd = [
                sys.executable,
                "-m",
                CLI_MODULE,
                source,
                "-o",
                str(out_path),
                "--model",
                options.model,
                "--min-words",
                str(options.min_words),
            ]
            for flag, value in (
                ("--language", options.language),
                ("--min-speakers", options.min_speakers),
                ("--max-speakers", options.max_speakers),
            ):
                if value:
                    cmd += [flag, str(value)]

            code = subprocess.run(cmd).returncode
            if code != 0 or not out_path.exists():
                raise TranscriptionError(f"the transcription exited with code {code}.")
            rows = json.loads(out_path.read_text(encoding="utf-8"))
        return [Turn.from_dict(r) for r in rows]
