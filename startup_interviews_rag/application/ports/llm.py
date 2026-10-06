"""LLM port. Use cases depend on `LLMProvider` only; which provider answers
(Anthropic, OpenRouter...) is decided in the composition root."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal, get_args

from startup_interviews_rag.domain.errors import StartupInterviewsRagError

Effort = Literal["low", "medium", "high", "xhigh", "max"]
EFFORTS: tuple[Effort, ...] = get_args(Effort)
DEFAULT_EFFORT: Effort = "high"


class LLMError(StartupInterviewsRagError):
    """Refusal, truncation, transport failure or unparseable output. Adapters
    translate their SDK exceptions into it."""


@dataclass(frozen=True)
class StructuredRequest:
    system: str
    prompt: str  # stable part: adapters mark it cacheable
    schema: dict  # JSON schema the response must follow
    schema_name: str = "response"
    suffix: str | None = None  # volatile tail after the cached prefix
    effort: Effort = DEFAULT_EFFORT
    max_tokens: int = 64_000


@dataclass(frozen=True)
class TokenUsage:
    """Anthropic semantics: `input_tokens` excludes cache reads and writes."""

    input_tokens: int
    output_tokens: int
    cache_read_input_tokens: int = 0
    cache_creation_input_tokens: int = 0

    def to_dict(self) -> dict:
        return {
            "input_tokens": self.input_tokens,
            "cache_read_input_tokens": self.cache_read_input_tokens,
            "cache_creation_input_tokens": self.cache_creation_input_tokens,
            "output_tokens": self.output_tokens,
        }


@dataclass(frozen=True)
class StructuredResponse:
    data: dict  # parsed JSON, shaped by the request schema
    model: str  # model requested
    served_by: str  # model that actually answered (fallbacks)
    request_id: str | None
    usage: TokenUsage


class LLMProvider(ABC):
    """A language model that answers with JSON following a schema."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider id, e.g. "anthropic"."""

    @property
    @abstractmethod
    def model(self) -> str:
        """Model id as this provider names it; part of the cache key."""

    @abstractmethod
    def generate_structured(self, request: StructuredRequest) -> StructuredResponse:
        """One call. Raises LLMError on any failure."""
