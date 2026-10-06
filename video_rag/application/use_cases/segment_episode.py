import logging
import time
from datetime import UTC, datetime

from video_rag.application.ports.llm import (
    DEFAULT_EFFORT,
    Effort,
    LLMProvider,
    StructuredRequest,
)
from video_rag.application.ports.repositories import (
    LLMInputRepository,
    SegmentationRepository,
    StorageError,
)
from video_rag.domain.segmentation import (
    PROMPT_VERSION,
    SYSTEM_PROMPT,
    output_schema,
    retry_feedback,
)

log = logging.getLogger(__name__)

MAX_TOKENS = 64_000


class SegmentEpisode:
    """Step 2 of docs/llm-ingestion.md: one LLM call per episode that returns
    where to cut it and the metadata of each unit.

    The record is cached with `model` and `prompt_version`: if both match,
    the LLM is not called again. Bumping PROMPT_VERSION or switching model
    (or provider, whose model ids differ) invalidates it."""

    def __init__(
        self, llm: LLMProvider, llm_inputs: LLMInputRepository, segments: SegmentationRepository
    ) -> None:
        self._llm = llm
        self._llm_inputs = llm_inputs
        self._segments = segments

    def episodes(self) -> list[str]:
        return self._llm_inputs.list_ids()

    def execute(
        self,
        video_id: str,
        effort: Effort = DEFAULT_EFFORT,
        force: bool = False,
        errors: list[str] | None = None,
    ) -> dict:
        """Returns the segments/<id>.json record. With `errors` (step 3
        retry) it always calls the LLM, showing it its previous response."""
        previous = self._cached(video_id)
        if previous and not force and not errors:
            log.info(f"{video_id}: cached ({PROMPT_VERSION}, {self._llm.model}), skipping LLM call")
            return previous

        llm_input = self._llm_inputs.get(video_id)
        if llm_input is None:
            raise StorageError(f"no LLM input for {video_id} (run prepare.py first).")
        labels = llm_input.speaker_labels

        suffix = None
        if errors:
            suffix = retry_feedback(errors, previous["response"] if previous else None)

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
                suffix=suffix,
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
