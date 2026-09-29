# Scribe Guard

Detects hallucinations (unsupported or altered content) and omissions
(missing clinically important facts) in AI-generated clinical notes
produced by ambient scribe systems.

## Status

🚧 In development. Phase 0: setup and literature review.

## Approach (planned)

- Detector 1: claim-level verification of note content against the transcript
- Detector 2: fact enumeration from the transcript with severity-graded omission checks
- Evaluation on a synthetic error-injected dataset built from ACI-BENCH transcripts

## Getting started

Requires Python 3.11 or newer.

```bash
git clone https://github.com/aayushhiiiiii/scribe-guard.git
cd scribe-guard
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```
