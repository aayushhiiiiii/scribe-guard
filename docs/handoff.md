2026-09-30: Encounter model added to schemas.py (frozen, extra="forbid";
names excluded for data minimization). 10 tests passing. Commit d623779.
NEXT: write loader in src/scribe_guard/data.py: read train.csv +
train_metadata.csv, join on encounter_id, rename columns (dataset→subset,
id→source_id, cc→chief_complaint, 2nd_complaints→secondary_complaints),
convert NaN→None, return list[Encounter]. Then loader tests, then open PR.
