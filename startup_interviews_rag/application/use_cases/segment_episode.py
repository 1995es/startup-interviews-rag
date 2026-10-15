import logging
import time
from datetime import UTC, datetime

from startup_interviews_rag.application.ports.llm import (
    DEFAULT_EFFORT,
    Effort,
    LLMProvider,
    StructuredRequest,
)
from startup_interviews_rag.application.ports.repositories import (
    LLMInputRepository,
    SegmentationRepository,
    StorageError,
)
from startup_interviews_rag.domain.numbering import LLMInput
from startup_interviews_rag.domain.segmentation import (
    PROMPT_VERSION,
    SYSTEM_PROMPT,
    output_schema,
    retry_feedback,
)
from startup_interviews_rag.domain.validation import validate_segmentation

log = logging.getLogger(__name__)

MAX_TOKENS = 64_000


class SegmentEpisode:
    """Steps 2 and 3 of docs/llm-ingestion.md: one LLM call per episode that
    returns where to cut it and the metadata of each unit, then deterministic
    validation of that response.

    A response that fails validation is retried once, with the errors and
    the previous response appended to the prompt. If the retry fails too, the
    record keeps the errors and `segmenter: "deterministic"`: the episode
    goes through the deterministic ingestion instead.

    The record is cached with `model` and `prompt_version`: if both match,
    the LLM is not called again (unless a failed first attempt still has its
    retry pending). Bumping PROMPT_VERSION or switching model (or provider,
    whose model ids differ) invalidates it."""

    def __init__(
        self, llm: LLMProvider, llm_inputs: LLMInputRepository, segments: SegmentationRepository
    ) -> None:
        self._llm = llm
        self._llm_inputs = llm_inputs
        self._segments = segments

    def episodes(self) -> list[str]:
        return self._llm_inputs.list_ids()

    def execute(self, video_id: str, effort: Effort = DEFAULT_EFFORT, force: bool = False) -> dict:
        """Returns the validated segments/<id>.json record."""
        llm_input = self._llm_inputs.get(video_id)
        if llm_input is None:
            raise StorageError(f"no LLM input for {video_id} (run prepare.py first).")

        record = None if force else self._cached(video_id)
        if record is None:
            record = self._call(llm_input, effort)
        else:
            log.info(f"{video_id}: cached ({PROMPT_VERSION}, {self._llm.model}), skipping LLM call")

        errors = validate_segmentation(record["response"], llm_input)
        if errors and record["attempt"] == 1:
            _log_errors(f"{video_id}: validation failed, retrying once", errors)
            record = self._call(llm_input, effort, errors, record["response"])
            errors = validate_segmentation(record["response"], llm_input)

        validated = {
            **record,
            "validation_errors": errors,
            "segmenter": "deterministic" if errors else "llm",
        }
        if validated != record:
            self._segments.save(video_id, validated)
        if errors:
            _log_errors(
                f"{video_id}: validation failed after the retry, "
                "falling back to deterministic ingestion",
                errors,
            )
        return validated

    def _call(
        self,
        llm_input: LLMInput,
        effort: Effort,
        errors: list[str] | None = None,
        previous: dict | None = None,
    ) -> dict:
        """One LLM call. The record is saved right away, so a paid response
        survives a failure later on."""
        video_id = llm_input.video_id
        labels = llm_input.speaker_labels
        log.info(
            f"{video_id}: calling {self._llm.name}/{self._llm.model} "
            f"({len(llm_input.units)} IDs, {len(labels)} speakers, "
            f"effort={effort}{', retry' if errors else ''}) ..."
        )
        t0 = time.monotonic()
        response = self._llm.generate_structured(
            StructuredRequest(
                system=SYSTEM_PROMPT,
                prompt=llm_input.prompt,
                schema=output_schema(labels),
                schema_name="episode_segmentation",
                suffix=retry_feedback(errors, previous) if errors else None,
                effort=effort,
                max_tokens=MAX_TOKENS,
            )
        )

        record = {
            "video_id": video_id,
            "provider": self._llm.name,
            "model": self._llm.model,
            "served_by": response.served_by,
            "prompt_version": PROMPT_VERSION,
            "created": datetime.now(UTC).isoformat(timespec="seconds"),
            "attempt": 2 if errors else 1,
            "request_id": response.request_id,
            "usage": response.usage.to_dict(),
            "response": response.data,
        }
        if errors:
            record["first_attempt_errors"] = errors
        location = self._segments.save(video_id, record)

        usage = response.usage
        fallback = (
            f", served by {response.served_by}" if response.served_by != response.model else ""
        )
        log.info(
            f"{video_id}: {len(response.data['units'])} units in "
            f"{time.monotonic() - t0:.0f} s ({usage.input_tokens} in + "
            f"{usage.cache_read_input_tokens} cached, {usage.output_tokens} out"
            f"{fallback}) -> {location}"
        )
        return record

    def _cached(self, video_id: str) -> dict | None:
        record = self._segments.get(video_id)
        if record is None:
            return None
        ok = (
            record.get("model") == self._llm.model
            and record.get("prompt_version") == PROMPT_VERSION
        )
        return record if ok else None


def _log_errors(message: str, errors: list[str]) -> None:
    log.info(f"{message}:")
    for error in errors:
        log.info(f"  - {error}")
