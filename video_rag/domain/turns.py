"""Speaker turns are cut per word, not per segment: a Whisper segment lasts
~20 s and usually holds both a question and its answer, so grouping by
segment speaker destroys the dialogue (643 fake turns vs. 547 real ones in
the sample video)."""

import re

from video_rag.domain.transcript import DEFAULT_SPEAKER, TranscriptSegment, Turn, Word

SENT_END = re.compile(r"[.!?…:;]+[\"')\]]*$")

Run = list[Word]


def group_runs(words: list[Word]) -> list[Run]:
    runs: list[Run] = []
    for w in words:
        if runs and runs[-1][0].speaker == w.speaker:
            runs[-1].append(w)
        else:
            runs.append([w])
    return runs


def smooth_runs(runs: list[Run], min_words: int) -> list[Run]:
    """Diarization flips speaker on isolated words: runs shorter than
    `min_words` are absorbed into the longer neighbour."""
    for _ in range(10):
        if len(runs) < 2:
            break
        changed = False
        for i, run in enumerate(runs):
            if len(run) >= min_words:
                continue
            prev_run = runs[i - 1] if i > 0 else None
            next_run = runs[i + 1] if i + 1 < len(runs) else None
            if next_run is None or (prev_run and len(prev_run) >= len(next_run)):
                target = prev_run
            else:
                target = next_run
            if target is None:
                continue
            for w in run:
                w.speaker = target[0].speaker
            changed = True
        if not changed:
            break
        runs = group_runs([w for r in runs for w in r])
    return runs


def snap_to_sentences(runs: list[Run], window: int = 3) -> list[Run]:
    """Speaker changes often land mid-sentence; move the boundary to the
    nearest sentence end within `window` words."""
    for i in range(len(runs) - 1):
        a, b = runs[i], runs[i + 1]
        if not a or not b or SENT_END.search(a[-1].text):
            continue

        fwd = next(
            (k for k in range(1, min(window, len(b) - 1) + 1) if SENT_END.search(b[k - 1].text)),
            None,
        )
        bwd = next(
            (
                j
                for j in range(1, min(window, len(a) - 1) + 1)
                if SENT_END.search(a[len(a) - j - 1].text)
            ),
            None,
        )

        if fwd is not None and (bwd is None or fwd <= bwd):
            moved, b[:] = b[:fwd], b[fwd:]
            for w in moved:
                w.speaker = a[0].speaker
            a.extend(moved)
        elif bwd is not None:
            moved, a[:] = a[len(a) - bwd :], a[: len(a) - bwd]
            for w in moved:
                w.speaker = b[0].speaker
            b[:0] = moved
    return [r for r in runs if r]


def build_turns(segments: list[TranscriptSegment], min_words: int) -> list[Turn]:
    """Rebuilds turns from word-level speakers, then smooths isolated speaker
    flips and snaps boundaries to sentence ends. Without word timings it
    falls back to one turn per segment."""
    words: list[Word] = []
    speaker = None
    for seg in segments:
        for w in seg.words:
            text = (w.text or "").strip()
            if not text:
                continue
            speaker = w.speaker or seg.speaker or speaker
            words.append(Word(text=text, speaker=speaker, start=w.start, end=w.end))

    if not words:
        return [
            Turn(
                text=(s.text or "").strip(),
                speaker=s.speaker or DEFAULT_SPEAKER,
                start=s.start,
                end=s.end,
            )
            for s in segments
            if (s.text or "").strip()
        ]

    # Leading words before the first diarized one belong to that same speaker.
    first = next((w.speaker for w in words if w.speaker), DEFAULT_SPEAKER)
    for w in words:
        w.speaker = w.speaker or first

    runs = snap_to_sentences(smooth_runs(group_runs(words), min_words))
    return [
        Turn(
            text=" ".join(w.text for w in r),
            speaker=r[0].speaker,
            start=next((w.start for w in r if w.start is not None), None),
            end=next((w.end for w in reversed(r) if w.end is not None), None),
        )
        for r in runs
    ]
