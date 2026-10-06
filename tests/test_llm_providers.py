"""Both adapters against stub SDK clients: request shape and response
mapping, no network."""

import json
from types import SimpleNamespace as NS

import pytest

from startup_interviews_rag.application.ports.llm import LLMError, StructuredRequest
from startup_interviews_rag.infrastructure.llm.anthropic_provider import AnthropicProvider
from startup_interviews_rag.infrastructure.llm.openrouter_provider import OpenRouterProvider

REQUEST = StructuredRequest(
    system="sys",
    prompt="transcript",
    schema={"type": "object"},
    schema_name="seg",
    suffix="retry tail",
    effort="xhigh",
    max_tokens=1000,
)
DATA = {"units": []}
DATA_JSON = json.dumps(DATA)


class StubAnthropic:
    def __init__(self, message):
        self.message, self.kwargs = message, None
        self.beta = NS(messages=NS(stream=self._stream))

    def _stream(self, **kwargs):
        self.kwargs = kwargs
        message = self.message

        class Stream:
            def __enter__(self):
                return NS(get_final_message=lambda: message, request_id="req_a")

            def __exit__(self, *exc):
                return False

        return Stream()


def anthropic_message(stop_reason="end_turn", text=DATA_JSON):
    return NS(
        stop_reason=stop_reason,
        stop_details=None,
        model="claude-opus-5",
        content=[NS(type="thinking"), NS(type="text", text=text)],
        usage=NS(
            input_tokens=10,
            output_tokens=3,
            cache_read_input_tokens=None,
            cache_creation_input_tokens=7,
        ),
    )


def test_anthropic_request_and_response():
    client = StubAnthropic(anthropic_message())
    response = AnthropicProvider("k", "claude-opus-5-5", client=client).generate_structured(REQUEST)

    kw = client.kwargs
    assert kw["model"] == "claude-opus-5-5" and kw["system"] == "sys"
    assert kw["messages"][0]["content"] == [
        {"type": "text", "text": "transcript", "cache_control": {"type": "ephemeral"}},
        {"type": "text", "text": "retry tail"},
    ]
    assert kw["output_config"] == {
        "effort": "xhigh",
        "format": {"type": "json_schema", "schema": {"type": "object"}},
    }
    assert kw["fallbacks"] == "default"

    assert response.data == DATA and response.request_id == "req_a"
    assert (response.model, response.served_by) == ("claude-opus-5-5", "claude-opus-5")
    assert response.usage.cache_read_input_tokens == 0
    assert response.usage.cache_creation_input_tokens == 7


@pytest.mark.parametrize(
    "message",
    [
        anthropic_message("refusal"),
        anthropic_message("max_tokens"),
        anthropic_message(text="{not json"),
    ],
)
def test_anthropic_failures_raise_llm_error(message):
    with pytest.raises(LLMError):
        AnthropicProvider("k", client=StubAnthropic(message)).generate_structured(REQUEST)


class StubOpenAI:
    def __init__(self, completion):
        self.completion, self.kwargs = completion, None
        self.chat = NS(completions=NS(create=self._create))

    def _create(self, **kwargs):
        self.kwargs = kwargs
        return self.completion


def completion(finish_reason="stop", content=DATA_JSON, refusal=None):
    usage = NS(
        prompt_tokens=100,
        completion_tokens=9,
        prompt_tokens_details=NS(cached_tokens=60, cache_write_tokens=30),
    )
    return NS(
        id="gen_1",
        model="anthropic/claude-opus-5-5",
        usage=usage,
        choices=[NS(finish_reason=finish_reason, message=NS(content=content, refusal=refusal))],
    )


def test_openrouter_request_and_response():
    client = StubOpenAI(completion())
    response = OpenRouterProvider("k", client=client).generate_structured(REQUEST)

    kw = client.kwargs
    assert kw["model"] == "anthropic/claude-opus-5-5"
    assert kw["messages"][0] == {"role": "system", "content": "sys"}
    assert kw["messages"][1]["content"][0]["cache_control"] == {"type": "ephemeral"}
    assert kw["messages"][1]["content"][1]["text"] == "retry tail"
    assert kw["response_format"]["json_schema"] == {
        "name": "seg",
        "strict": True,
        "schema": {"type": "object"},
    }
    assert kw["extra_body"] == {"reasoning": {"effort": "xhigh"}}

    assert response.data == DATA and response.request_id == "gen_1"
    # prompt_tokens includes cached and written tokens; the port's does not.
    assert response.usage.input_tokens == 10
    assert response.usage.cache_read_input_tokens == 60
    assert response.usage.cache_creation_input_tokens == 30


@pytest.mark.parametrize(
    "bad",
    [
        completion("length"),
        completion("content_filter"),
        completion(refusal="no"),
        completion(content=None),
    ],
)
def test_openrouter_failures_raise_llm_error(bad):
    with pytest.raises(LLMError):
        OpenRouterProvider("k", client=StubOpenAI(bad)).generate_structured(REQUEST)
