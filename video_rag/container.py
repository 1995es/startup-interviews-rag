"""Composition root: the only place that picks concrete adapters and wires
them into the use cases. Interfaces (CLI now, API later) ask for a use case
here and never import infrastructure themselves.

Heavy adapters (WhisperX/torch, the LLM SDKs) are imported inside the
factories, so building one use case does not load the others' stacks.
"""

from video_rag.application.ports.llm import LLMProvider
from video_rag.application.use_cases.prepare_llm_input import PrepareLLMInput
from video_rag.application.use_cases.render_script import RenderScript
from video_rag.application.use_cases.segment_episode import SegmentEpisode
from video_rag.application.use_cases.transcribe_video import TranscribeVideo
from video_rag.config import ConfigError, Settings
from video_rag.infrastructure.persistence.json_repositories import (
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
        from video_rag.infrastructure.llm.anthropic_provider import DEFAULT_MODEL, AnthropicProvider

        return AnthropicProvider(
            _require(settings.anthropic_api_key, "ANTHROPIC_API_KEY"),
            settings.llm_model or DEFAULT_MODEL,
        )
    if provider == "openrouter":
        from video_rag.infrastructure.llm.openrouter_provider import (
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


def transcribe_video(settings: Settings) -> TranscribeVideo:
    from video_rag.infrastructure.audio.ytdlp_audio_source import YtDlpAudioSource
    from video_rag.infrastructure.transcription.whisperx_recognizer import WhisperXRecognizer

    return TranscribeVideo(
        audio=YtDlpAudioSource(settings.audio_dir),
        recognizer=WhisperXRecognizer(hf_token=settings.hf_token),
        transcripts=JsonTranscriptRepository(settings.transcripts_dir),
    )


def render_script(settings: Settings) -> RenderScript:
    return RenderScript(JsonTranscriptRepository(settings.transcripts_dir))


def prepare_llm_input(settings: Settings) -> PrepareLLMInput:
    from video_rag.infrastructure.metadata.ytdlp_metadata_source import YtDlpMetadataSource
    from video_rag.infrastructure.transcription.subprocess_transcriber import SubprocessTranscriber

    return PrepareLLMInput(
        metadata_source=YtDlpMetadataSource(),
        metadata=JsonMetadataRepository(settings.meta_dir),
        transcriber=SubprocessTranscriber(),
        transcripts=JsonTranscriptRepository(settings.transcripts_dir),
        llm_inputs=FileLLMInputRepository(settings.llm_input_dir),
    )


def segment_episode(settings: Settings) -> SegmentEpisode:
    return SegmentEpisode(
        llm=build_llm(settings),
        llm_inputs=FileLLMInputRepository(settings.llm_input_dir),
        segments=JsonSegmentationRepository(settings.segments_dir),
    )
