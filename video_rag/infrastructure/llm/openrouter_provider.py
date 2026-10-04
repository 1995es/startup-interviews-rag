"""`LLMProvider` on OpenRouter's OpenAI-compatible Chat Completions API.

- Structured output goes through `response_format` (json_schema, strict).
- `reasoning.effort` accepts the same levels as the port (low..max).
- `cache_control` on the prompt part enables prompt caching on providers
  that need explicit breakpoints (Anthropic models); the rest cache
  automatically or ignore it.
"""

import openai

from video_rag.application.ports.llm import (
    LLMError,
    LLMProvider,
    StructuredRequest,
    StructuredResponse,
    TokenUsage,
)
from video_rag.infrastructure.llm._common import parse_json, user_content

BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "anthropic/claude-opus-5-5"

# A whole episode at high effort can run for several minutes; the call is
# not streamed, so the SDK default (10 min) is too tight.
TIMEOUT_S = 30 * 60


class OpenRouterProvider(LLMProvider):
    def __init__(
        self, api_key: str, model: str = DEFAULT_MODEL, client: openai.OpenAI | None = None
    ) -> None:
        self._model = model
        self._client = client or openai.OpenAI(
            api_key=api_key, base_url=BASE_URL, timeout=TIMEOUT_S
        )

    @property
    def name(self) -> str:
        return "openrouter"

    @property
    def model(self) -> str:
        return self._model

    def generate_structured(self, request: StructuredRequest) -> StructuredResponse:
        try:
            completion = self._client.chat.completions.create(
                model=self._model,
                max_tokens=request.max_tokens,
                messages=[
                    {"role": "system", "content": request.system},
                    {"role": "user", "content": user_content(request)},
                ],
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": request.schema_name,
                        "strict": True,
                        "schema": request.schema,
                    },
                },
                extra_body={"reasoning": {"effort": request.effort}},
            )
        except openai.OpenAIError as exc:
            raise LLMError(f"{type(exc).__name__}: {exc}") from exc

        if not completion.choices:
            raise LLMError("response has no choices")
        choice = completion.choices[0]
        if choice.finish_reason == "content_filter" or choice.message.refusal:
            raise LLMError(f"model refusal ({choice.message.refusal or 'content_filter'})")
        if choice.finish_reason == "length":
            raise LLMError(f"response truncated at max_tokens={request.max_tokens}")

        text = choice.message.content
        if not text:
            raise LLMError(f"response has no text (finish_reason={choice.finish_reason})")

        return StructuredResponse(
            data=parse_json(text),
            model=self._model,
            served_by=completion.model or self._model,
            request_id=completion.id,
            usage=_usage(completion.usage),
        )


def _usage(usage) -> TokenUsage:
    """OpenAI-style usage counts cached tokens inside `prompt_tokens`; the
    port follows Anthropic, where `input_tokens` excludes them."""
    if usage is None:
        return TokenUsage(0, 0)
    details = usage.prompt_tokens_details
    cached = (details.cached_tokens or 0) if details else 0
    written = (details.cache_write_tokens or 0) if details else 0
    return TokenUsage(
        input_tokens=max(usage.prompt_tokens - cached - written, 0),
        output_tokens=usage.completion_tokens,
        cache_read_input_tokens=cached,
        cache_creation_input_tokens=written,
    )
