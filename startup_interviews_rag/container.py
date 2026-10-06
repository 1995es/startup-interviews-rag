"""Composition root: the only place that picks concrete adapters and wires
them into the use cases. Interfaces (CLI now, API later) ask for a use case
here and never import infrastructure themselves.

Heavy adapters (WhisperX/torch, the LLM SDKs) are imported inside the
factories, so building one use case does not load the others' stacks.
"""

from startup_interviews_rag.application.ports.llm import LLMProvider
from startup_interviews_rag.application.ports.transcription import SpeechRecognizer
from startup_interviews_rag.application.use_cases.prepare_llm_input import PrepareLLMInput
from startup_interviews_rag.application.use_cases.render_script import RenderScript
from startup_interviews_rag.application.use_cases.segment_episode import SegmentEpisode
from startup_interviews_rag.config import ConfigError, Settings
from startup_interviews_rag.infrastructure.persistence.json_repositories import (
    FileLLMInputRepository,
    JsonMetadataRepository,
    JsonSegmentationRepository,
    JsonTranscriptRepository,
)

LLM_PROVIDERS = ("anthropic", "openrouter")


def _require(value: str | None, var: str) -> str:
    if not value:
        raise ConfigError(f"{var} is not set (add it to .env).")
    return value


def build_llm(settings: Settings) -> LLMProvider:
    provider = settings.llm_provider
    if provider == "anthropic":
        from startup_interviews_rag.infrastructure.llm.anthropic_provider import (
            DEFAULT_MODEL,
            AnthropicProvider,
        )

        return AnthropicProvider(
            _require(settings.anthropic_api_key, "ANTHROPIC_API_KEY"),
            settings.llm_model or DEFAULT_MODEL,
        )
    if provider == "openrouter":
        from startup_interviews_rag.infrastructure.llm.openrouter_provider import (
            DEFAULT_MODEL,
            OpenRouterProvider,
        )

        return OpenRouterProvider(
            _require(settings.openrouter_api_key, "OPENROUTER_API_KEY"),
            settings.llm_model or DEFAULT_MODEL,
        )
    raise ConfigError(
        f"unknown LLM provider '{provider}' (expected one of: {', '.join(LLM_PROVIDERS)})."
    )


def render_script(settings: Settings) -> RenderScript:
    return RenderScript(JsonTranscriptRepository(settings.transcripts_dir))


def _whisperx(settings: Settings) -> SpeechRecognizer:
    from startup_interviews_rag.infrastructure.transcription.whisperx_recognizer import (
        WhisperXRecognizer,
    )

    return WhisperXRecognizer(hf_token=settings.hf_token)


def prepare_llm_input(settings: Settings) -> PrepareLLMInput:
    from startup_interviews_rag.infrastructure.audio.ytdlp_audio_source import YtDlpAudioSource
    from startup_interviews_rag.infrastructure.metadata.ytdlp_metadata_source import (
        YtDlpMetadataSource,
    )
    from startup_interviews_rag.infrastructure.transcription.lazy_recognizer import LazyRecognizer

    return PrepareLLMInput(
        metadata_source=YtDlpMetadataSource(),
        metadata=JsonMetadataRepository(settings.meta_dir),
        audio=YtDlpAudioSource(settings.audio_dir),
        # WhisperX is only imported if there is something to transcribe
        recognizer=LazyRecognizer(lambda: _whisperx(settings)),
        transcripts=JsonTranscriptRepository(settings.transcripts_dir),
        llm_inputs=FileLLMInputRepository(settings.llm_input_dir),
    )


def segment_episode(settings: Settings) -> SegmentEpisode:
    return SegmentEpisode(
        llm=build_llm(settings),
        llm_inputs=FileLLMInputRepository(settings.llm_input_dir),
        segments=JsonSegmentationRepository(settings.segments_dir),
    )
