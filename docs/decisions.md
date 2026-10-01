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

## 003: Evaluate at fixed false-alarm rates with frozen thresholds

**Status:** Proposed. To be written.

Report detection performance at fixed false-alarm rates, separately for
hallucinations and omissions. Tune thresholds on the dev split, freeze them,
and report once on the held-out test split.

## 004: Transcript version used as evidence for the aci subset

**Status:** Proposed. To be written.

Leading option: ASR-corrected transcripts as the main evidence source, with a
raw-ASR robustness test on valid/test only (train has no raw aci ASR file).

## 005: Represent patient age as value plus explicit unit

**Status:** Accepted (2026-09-30)

**Context:** The Encounter model originally stored age as an integer number of
years. Validating all five challenge_data splits showed that two pediatric ages
are recorded in months (`22-month` in valid, `9-month` in
clinicalnlp_taskB_test1). A survey of every metadata file found no other formats.

**Decision:** Store age as a nested `Age` model with `value` (non-negative
integer) and `unit` (`"years"` or `"months"`). The loader parses the two
observed formats; any other format raises an error naming the encounter.

**Alternatives considered:**

- Convert everything to years as a float: simpler, but discards the source
  unit and implies false precision (22 months becomes 1.83 years).
- Keep the raw text: no parsing, but no validation, and it pushes format
  handling into every downstream component.

**Consequences:**

- Lossless and strictly validated; mirrors FHIR's value-plus-unit approach.
- The range limit (0–120) applies to both units, so implausible values like
  110 months are not rejected. Accepted for now: only 9 and 22 months occur.
- New formats (e.g. weeks) require an explicit code change, by design.
- Detector relevance: unit errors (e.g. "22-year-old" vs. "22 months") are a
  hallucination type the numeric rules should cover in Phase 2.
