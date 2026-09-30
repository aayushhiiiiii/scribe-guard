# Data Provenance

## ACI-BENCH

| Field      | Value                                                                                                                           |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Source     | Figshare, https://doi.org/10.6084/m9.figshare.22494601                                                                          |
| Version    | v1, posted 2023-07-08 (versioned DOI: 10.6084/m9.figshare.22494601.v1)                                                                                                    |
| Downloaded | 2026-09-29                                                                                                                      |
| License    | CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/), as stated on the Figshare page; the download contains no license file |
| Local path | `data/raw/aci-bench-corpus/` (gitignored)                                                                                       |
| Size       | 47 files, ~4.3 MB                                                                                                               |
| Integrity  | SHA-256 manifest in `docs/aci-bench-sha256.txt`                                                                                 |

**Citation:** Yim, W., Fu, Y., Ben Abacha, A., Snider, N., Lin, T., & Yetisgen, M. (2023). ACI-BENCH: a Novel Ambient Clinical Intelligence Dataset for Benchmarking Automatic Visit Note Generation. _Scientific Data_, 10, 586.

### Contents

- 207 dialogue–note encounter pairs (source: README.txt in the download).
- `challenge_data/`: the train, valid, and three test splits used in the MEDIQA-Chat 2023 (ClinicalNLP) and MEDIQA-Sum (ImageCLEF 2023) shared tasks. Each split has a data CSV (id, dialogue, note) and a `_metadata.csv`.
- `src_experiment_data/`: per-subset files with alternative transcript versions (ASR, ASR-corrected, human transcription), for the paper's ASR experiments.

### Handling notes

- The browser auto-extracted the download; the original zip was not retained. Integrity is therefore recorded per file rather than for the archive.
- `data/raw/` is kept exactly as downloaded. All derived files go in `data/processed/` and are produced by code.
- The data is synthetic (expert-written or role-played encounters; no real patients), so no PHI is involved.

### Observations from the initial audit

- No `virtassist` files exist in `src_experiment_data/`. Likely because virtassist has only one transcript version; to be verified against the metadata in Phase 1 Step 2.
- `train` has no raw-ASR version of the aci subset, so any raw-ASR robustness test can only run on valid/test splits (relevant to decision 004).
- The test splits have been public shared-task data since 2023, so LLM pretraining contamination is possible.

### How to verify your copy

From `data/raw/`, run:

    shasum -a 256 -c ../../docs/aci-bench-sha256.txt

Every line should end in `OK`.
