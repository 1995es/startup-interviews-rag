"""`LLMProvider` on the Anthropic Messages API.

Model notes (claude-opus-5-5):
- It rejects `temperature` (the API returns 400), so it is not pinned to 0.
  Adaptive thinking cannot be disabled; depth is controlled with `effort`,
  whose default on this model is `medium`, so it is always sent.
- `fallbacks: "default"` is enabled: if a safety classifier declines the
  request, the API reruns it on the matching fallback model. The model that
  actually answered comes back as `served_by`.
"""

import anthropic

from startup_interviews_rag.application.ports.llm import (
    LLMError,
    LLMProvider,
    StructuredRequest,
    StructuredResponse,
    TokenUsage,
)
from startup_interviews_rag.infrastructure.llm._common import parse_json, user_content

DEFAULT_MODEL = "claude-opus-5-5"


class AnthropicProvider(LLMProvider):
    def __init__(
        self, api_key: str, model: str = DEFAULT_MODEL, client: anthropic.Anthropic | None = None
    ) -> None:
        self._model = model
        self._client = client or anthropic.Anthropic(api_key=api_key)

    @property
    def name(self) -> str:
        return "anthropic"

    @property
    def model(self) -> str:
        return self._model

    def generate_structured(self, request: StructuredRequest) -> StructuredResponse:
        try:
            with self._client.beta.messages.stream(
                model=self._model,
                max_tokens=request.max_tokens,
                system=request.system,
                messages=[{"role": "user", "content": user_content(request)}],
                thinking={"type": "adaptive"},
                output_config={
                    "effort": request.effort,
                    "format": {"type": "json_schema", "schema": request.schema},
                },
                betas=["server-side-fallback-2026-07-01"],
                fallbacks="default",
            ) as stream:
                message = stream.get_final_message()
                # A streamed message is assembled from SSE events, so it has
                # no `_request_id`; the header lives on the stream.
                request_id = stream.request_id
        except anthropic.APIError as exc:
            raise LLMError(f"{type(exc).__name__}: {exc}") from exc

        if message.stop_reason == "refusal":
            category = message.stop_details.category if message.stop_details else None
            raise LLMError(f"model refusal (category: {category})")
        if message.stop_reason == "max_tokens":
            raise LLMError(f"response truncated at max_tokens={request.max_tokens}")

        text = next((b.text for b in message.content if b.type == "text"), None)
        if text is None:
            raise LLMError(f"response has no text (stop_reason={message.stop_reason})")

        usage = message.usage
        return StructuredResponse(
            data=parse_json(text),
            model=self._model,
            served_by=message.model,
            request_id=request_id,
            usage=TokenUsage(
                input_tokens=usage.input_tokens,
                output_tokens=usage.output_tokens,
                cache_read_input_tokens=usage.cache_read_input_tokens or 0,
                cache_creation_input_tokens=usage.cache_creation_input_tokens or 0,
            ),
        )
