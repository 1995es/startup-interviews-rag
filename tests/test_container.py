import pytest

from startup_interviews_rag import container
from startup_interviews_rag.config import ConfigError, Settings
from startup_interviews_rag.infrastructure.llm.anthropic_provider import AnthropicProvider
from startup_interviews_rag.infrastructure.llm.openrouter_provider import OpenRouterProvider


def test_provider_is_chosen_by_settings():
    llm = container.build_llm(Settings(anthropic_api_key="a"))
    assert isinstance(llm, AnthropicProvider) and llm.model == "claude-opus-5-5"

    llm = container.build_llm(
        Settings(llm_provider="openrouter", openrouter_api_key="o", llm_model="openai/gpt-x")
    )
    assert isinstance(llm, OpenRouterProvider) and llm.model == "openai/gpt-x"


def test_segment_episode_gets_the_configured_provider():
    use_case = container.segment_episode(
        Settings(llm_provider="openrouter", openrouter_api_key="o")
    )
    assert use_case._llm.name == "openrouter"


@pytest.mark.parametrize(
    "settings",
    [
        Settings(),
        Settings(llm_provider="openrouter"),
        Settings(llm_provider="nope", anthropic_api_key="a"),
    ],
)
def test_bad_configuration_raises(settings):
    with pytest.raises(ConfigError):
        container.build_llm(settings)


def test_prepare_llm_input_does_not_load_whisperx_until_needed(monkeypatch):
    import sys

    module = "startup_interviews_rag.infrastructure.transcription.whisperx_recognizer"
    monkeypatch.delitem(sys.modules, module, raising=False)  # other tests import it
    container.prepare_llm_input(Settings())
    assert module not in sys.modules
