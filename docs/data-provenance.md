# Data Provenance

## ACI-BENCH

| Field      | Value                                                                                                                           |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Source     | Figshare, https://doi.org/10.6084/m9.figshare.22494601                                                                          |
| Version    | v1, posted 2023-07-08 (versioned DOI: 10.6084/m9.figshare.22494601.v1)                                                          |
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

## Observed structure: challenge_data/train (inspected 2026-09-30, pandas 3.0.6)

train.csv: 67 rows × 4 columns: `dataset`, `encounter_id`, `dialogue`, `note`.
The README lists `id, dialogue, note`; actual columns differ (no `id`, extra `dataset`).

- Subset counts (`dataset`): aci 35, virtassist 20, virtscribe 12.
- `encounter_id` is unique (format `D2N###`); used as primary key.

train_metadata.csv: 67 rows × 10 columns: `dataset`, `encounter_id`, `id`,
`doctor_name`, `patient_gender`, `patient_age`, `patient_firstname`,
`patient_familyname`, `cc`, `2nd_complaints`.

- `encounter_id` sets are identical across both files → join key.
- `id` appears to be a source-collection ID (e.g. `VA049` for virtassist).
  Interpretation, not verified.
- Missing values: doctor_name 60, patient_age 13, patient_familyname 20,
  2nd_complaints 24, patient_firstname 8, patient_gender 2; all others 0.
- `patient_age` loads as float64 because of NaN. Range 3–91, median 53 (n=54).
  1 encounter under 18 (D2N055, aci, age 3).

Format observations:

- Dialogue: one turn per line, `[doctor]` / `[patient]` tags; lowercase,
  unpunctuated, disfluent, includes small talk. Patient names spoken aloud.
- Note: ALL-CAPS section headers (e.g. CHIEF COMPLAINT, MEDICAL HISTORY,
  REVIEW OF SYSTEMS, PHYSICAL EXAM, ASSESSMENT AND PLAN); some bullets run
  together on one line.

Open questions:

- Which transcript version (ASR-corrected or raw ASR) is in challenge_data
  `dialogue` for aci?
- Which ID column do src_experiment_data files use?
- Virtassist single-version hypothesis: supported (20 virtassist encounters in
  train, no virtassist files in src_experiment_data), not confirmed.

## Observed structure: all challenge_data splits (verified 2026-09-30 via load_split)

| Split                   | virtassist | virtscribe | aci     | Total   |
| ----------------------- | ---------- | ---------- | ------- | ------- |
| train                   | 20         | 12         | 35      | 67      |
| valid                   | 5          | 4          | 11      | 20      |
| clinicalnlp_taskB_test1 | 10         | 8          | 22      | 40      |
| clinicalnlp_taskC_test2 | 10         | 8          | 22      | 40      |
| clef_taskC_test3        | 10         | 8          | 22      | 40      |
| **All**                 | **55**     | **40**     | **112** | **207** |

- Total of 207 confirmed by direct count (matches README.txt).
- 207 unique encounter_ids: no encounter appears in more than one challenge split.
- Every split: all data rows matched metadata on (encounter_id, dataset); no rows lost.
- `patient_age` formats: whole years (all splits) and `N-month` (valid: `22-month`,
  D2N076; clinicalnlp_taskB_test1: `9-month`). No other formats observed.
- Non-missing ages: train 54, valid 16, test1 35, test2 35, test3 32.
- At least 3 pediatric encounters (3 years, 9 months, 22 months). Too few to
  support any pediatric performance claim.
- Per-subset sizes still to confirm against paper Table 3.
