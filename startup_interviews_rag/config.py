import os
from dataclasses import dataclass
from pathlib import Path
from typing import Self

from dotenv import find_dotenv, load_dotenv

from startup_interviews_rag.domain.errors import StartupInterviewsRagError


class ConfigError(StartupInterviewsRagError):
    pass


@dataclass(frozen=True)
class Settings:
    """Runtime configuration. Folders are relative to the working directory
    (the project root when run through `poetry run`)."""

    llm_provider: str = "anthropic"
    llm_model: str | None = None  # None: the provider's default model
    anthropic_api_key: str | None = None
    openrouter_api_key: str | None = None
    hf_token: str | None = None
    audio_dir: Path = Path("audio")
    transcripts_dir: Path = Path("output")
    meta_dir: Path = Path("meta")
    llm_input_dir: Path = Path("llm_input")
    segments_dir: Path = Path("segments")

    @classmethod
    def from_env(cls) -> Self:
        """Reads the environment plus the nearest .env. Values in .env win
        over the shell, so a stale exported key cannot shadow it."""
        dotenv = find_dotenv(usecwd=True)
        if dotenv:
            load_dotenv(dotenv, override=True)
        env = os.environ.get
        return cls(
            llm_provider=(env("LLM_PROVIDER") or "anthropic").strip().lower(),
            llm_model=env("LLM_MODEL") or None,
            anthropic_api_key=env("ANTHROPIC_API_KEY") or None,
            openrouter_api_key=env("OPENROUTER_API_KEY") or None,
            hf_token=env("HF_TOKEN") or None,
        )
