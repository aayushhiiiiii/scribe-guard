"""Load ACI-BENCH challenge_data splits into validated Encounter objects."""

import re
from pathlib import Path

import pandas as pd
from pydantic import ValidationError

from scribe_guard.schemas import Age, Encounter

# CSV column name -> Encounter field name
COLUMN_MAP = {
    "dataset": "subset",
    "id": "source_id",
    "cc": "chief_complaint",
    "2nd_complaints": "secondary_complaints",
}

# Fields we keep. Name columns are dropped on purpose (data minimization).
KEEP_FIELDS = [
    "encounter_id",
    "source_id",
    "subset",
    "dialogue",
    "note",
    "chief_complaint",
    "secondary_complaints",
    "patient_age",
    "patient_gender",
]

# Age formats observed across all challenge_data splits (see data-provenance.md).
_YEARS_PATTERN = re.compile(r"(\d+)(\.0)?")
_MONTHS_PATTERN = re.compile(r"(\d+)-month")


def parse_age(raw: object) -> Age | None:
    """Convert a raw metadata age (e.g. 50.0, "50", "22-month") into an Age."""
    if raw is None:
        return None
    text = str(raw).strip()

    years = _YEARS_PATTERN.fullmatch(text)
    if years:
        return Age(value=int(years.group(1)), unit="years")

    months = _MONTHS_PATTERN.fullmatch(text)
    if months:
        return Age(value=int(months.group(1)), unit="months")

    raise ValueError(f"unrecognized age format: {text!r}")

def load_split(data_dir: Path, split: str) -> list[Encounter]:
    """Load one split (e.g. "train") from data_dir as validated Encounters."""
    data = pd.read_csv(data_dir / f"{split}.csv")
    meta = pd.read_csv(data_dir / f"{split}_metadata.csv")

    merged = data.merge(
        meta,
        on=["encounter_id", "dataset"],
        how="inner",
        validate="one_to_one",
    )
    if not (len(merged) == len(data) == len(meta)):
        raise ValueError(
            f"{split}: {len(data)} data rows, {len(meta)} metadata rows, "
            f"but only {len(merged)} matched on encounter_id and dataset"
        )

    merged = merged.rename(columns=COLUMN_MAP)[KEEP_FIELDS]

    encounters = []
    for record in merged.to_dict(orient="records"):
        clean = {key: (None if pd.isna(value) else value) for key, value in record.items()}
        try:
            clean["patient_age"] = parse_age(clean["patient_age"])
            encounters.append(Encounter(**clean))
        except (ValidationError, ValueError) as err:
            raise ValueError(f"{split}: invalid encounter {clean['encounter_id']}") from err
    return encounters