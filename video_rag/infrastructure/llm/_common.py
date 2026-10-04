"""Request and response pieces shared by the `LLMProvider` adapters."""

import json

from video_rag.application.ports.llm import LLMError, StructuredRequest


def user_content(request: StructuredRequest) -> list[dict]:
    """The prompt carries cache_control, so a retry with a different suffix
    reads the transcript from the prompt cache."""
    content = [{"type": "text", "text": request.prompt, "cache_control": {"type": "ephemeral"}}]
    if request.suffix:
        content.append({"type": "text", "text": request.suffix})
    return content


def parse_json(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise LLMError(f"response is not valid JSON: {exc}") from exc
