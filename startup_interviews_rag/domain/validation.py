"""Deterministic checks on the LLM segmentation (step 3 of
docs/llm-ingestion.md). The errors go back to the LLM on the single retry,
so each one names the unit (1-based, in response order) and the exact IDs.

The response is assumed to match the JSON schema (the provider enforces
it): these checks cover what a schema cannot express.
"""

from itertools import pairwise

from startup_interviews_rag.domain.numbering import LLMInput

MIN_UNIT_WORDS = 80
MAX_UNIT_WORDS = 600
FILLER = "relleno"  # exempt from the size limit: it is not indexed


def validate_segmentation(response: dict, llm_input: LLMInput) -> list[str]:
    """Returns the validation errors; an empty list means the segmentation
    can be cut into chunks."""
    ids = [u.id for u in llm_input.units]
    index = {id_: i for i, id_ in enumerate(ids)}
    split: dict[str, list[str]] = {}  # turn split into sentences -> its sentence IDs
    for u in llm_input.units:
        if u.id != u.turn:
            split.setdefault(u.turn, []).append(u.id)

    errors: list[str] = []
    spans: list[tuple[int, int, int, dict]] = []  # (unit number, from, to, unit)
    for n, unit in enumerate(response["units"], start=1):
        bounds = []
        for field in ("from", "to"):
            id_ = unit[field]
            if id_ in index:
                bounds.append(index[id_])
            elif id_ in split:
                sentences = split[id_]
                errors.append(
                    f"unit {n}: `{field}` {id_} is not a valid ID ({id_} is split into "
                    f"sentences: {sentences[0]}-{sentences[-1]})"
                )
            else:
                errors.append(f"unit {n}: `{field}` {id_} is not a valid ID")
        if len(bounds) < 2:
            continue
        start, end = bounds
        if start > end:
            errors.append(f"unit {n}: `from` {unit['from']} comes after `to` {unit['to']}")
            continue
        spans.append((n, start, end, unit))

    errors += _order_errors(spans)
    errors += _coverage_errors(spans, ids)
    errors += _size_errors(spans, llm_input)

    described = {s["label"] for s in response["speakers"]}
    errors += [
        f"`speakers` is missing {label}"
        for label in llm_input.speaker_labels
        if label not in described
    ]
    return errors


def _order_errors(spans: list[tuple[int, int, int, dict]]) -> list[str]:
    errors = []
    for (pn, pstart, _, prev), (n, start, _, unit) in pairwise(spans):
        if start < pstart:
            errors.append(
                f"unit {n} ({unit['from']}-{unit['to']}) starts before "
                f"unit {pn} ({prev['from']}-{prev['to']})"
            )
    return errors


def _coverage_errors(spans: list[tuple[int, int, int, dict]], ids: list[str]) -> list[str]:
    counts = [0] * len(ids)
    for _, start, end, _ in spans:
        for i in range(start, end + 1):
            counts[i] += 1

    errors = []
    uncovered = _ranges([i for i, c in enumerate(counts) if c == 0], ids)
    if uncovered:
        errors.append(f"not covered by any unit: {uncovered}")
    repeated = _ranges([i for i, c in enumerate(counts) if c > 1], ids)
    if repeated:
        errors.append(f"covered by more than one unit: {repeated}")
    return errors


def _size_errors(spans: list[tuple[int, int, int, dict]], llm_input: LLMInput) -> list[str]:
    errors = []
    for n, start, end, unit in spans:
        if unit["type"] == FILLER:
            continue
        count = sum(len(u.text.split()) for u in llm_input.units[start : end + 1])
        if not MIN_UNIT_WORDS <= count <= MAX_UNIT_WORDS:
            errors.append(
                f"unit {n} ({unit['from']}-{unit['to']}, {unit['type']}) has {count} words; "
                f"it must have {MIN_UNIT_WORDS}-{MAX_UNIT_WORDS} (only {FILLER} is exempt)"
            )
    return errors


def _ranges(positions: list[int], ids: list[str]) -> str:
    """Consecutive positions as compact ID ranges: "t001-t004, t009"."""
    groups: list[list[int]] = []
    for p in positions:
        if groups and p == groups[-1][-1] + 1:
            groups[-1].append(p)
        else:
            groups.append([p])
    return ", ".join(ids[g[0]] if len(g) == 1 else f"{ids[g[0]]}-{ids[g[-1]]}" for g in groups)
