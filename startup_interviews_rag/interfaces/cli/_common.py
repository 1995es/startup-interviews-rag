import argparse
import faulthandler
import functools
import logging
import sys
from collections.abc import Callable

from startup_interviews_rag.application.ports.transcription import TranscriptionOptions
from startup_interviews_rag.domain.errors import StartupInterviewsRagError


class _Formatter(logging.Formatter):
    """`[HH:MM:SS] message`, with the level in front of warnings and errors."""

    def format(self, record: logging.LogRecord) -> str:
        line = super().format(record)
        if record.levelno < logging.WARNING:
            return line
        stamp, _, message = line.partition(" ")
        return f"{stamp} {record.levelname}: {message}"


def configure_logging() -> None:
    """`[HH:MM:SS] message` on stdout, one line per record."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(_Formatter("[%(asctime)s] %(message)s", "%H:%M:%S"))
    root = logging.getLogger("startup_interviews_rag")
    root.handlers[:] = [handler]
    root.setLevel(logging.INFO)
    root.propagate = False


def cli_entrypoint(func: Callable[[], None]) -> Callable[[], None]:
    """Decorates a command's `main`: configures logging when the command
    runs (not on import) and turns expected failures into a one-line error
    instead of a traceback. faulthandler makes a native crash (CTranslate2
    segfault) print the Python stack instead of dying silently."""

    @functools.wraps(func)
    def wrapper() -> None:
        faulthandler.enable()
        configure_logging()
        try:
            func()
        except StartupInterviewsRagError as exc:
            sys.exit(f"ERROR: {exc}")

    return wrapper


def add_transcription_args(ap: argparse.ArgumentParser) -> None:
    """The WhisperX flags shared by every command that transcribes."""
    ap.add_argument(
        "--model", default=TranscriptionOptions.model, help="Whisper model (tiny..large-v3)"
    )
    ap.add_argument("--language", help="language code, e.g. en (auto-detected if omitted)")
    ap.add_argument("--min-speakers", type=int)
    ap.add_argument("--max-speakers", type=int)
    ap.add_argument(
        "--min-words",
        type=int,
        default=TranscriptionOptions.min_words,
        help="shorter turns are merged into their neighbour",
    )


def transcription_options(args: argparse.Namespace) -> TranscriptionOptions:
    return TranscriptionOptions(
        model=args.model,
        language=args.language,
        min_speakers=args.min_speakers,
        max_speakers=args.max_speakers,
        min_words=args.min_words,
    )
