# Design Decisions

## 001: Separate detectors for hallucinations and omissions

**Status:** Accepted

**Context:** AI scribe notes can fail in two ways: adding unsupported
content (hallucinations) or leaving out important facts (omissions).
Research shows LLM judges are good at checking whether something is
present but weak at noticing what's missing (Fox et al., 2026).

**Decision:** Build two separate detectors, each designed for one error type.

**Consequences:** Each detector can use the method that suits its task,
and results can be reported separately. The trade-off is more code to
build and maintain.

## 002: Build ground truth from transcripts, not ACI-BENCH reference notes

**Status:** Accepted

**Context:** ACI-BENCH includes reference clinical notes, but these
contain their own discrepancies compared to the transcripts.

**Decision:** Create the answer key from fact sheets derived directly
from the transcripts.

**Consequences:** The evaluation measures errors against what was
actually said. The trade-off is extra work to build the fact sheets.

## 003: Report detection at fixed false-alarm rates, split by error type

**Status:** Accepted

**Context:**

**Decision:**

**Consequences:**
