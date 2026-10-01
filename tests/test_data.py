from pathlib import Path

import pandas as pd
import pytest

from scribe_guard.data import load_split, parse_age
from scribe_guard.schemas import Age


# ---------- parse_age ----------

def test_parse_age_handles_years_months_and_missing():
    assert parse_age(50.0) == Age(value=50, unit="years")
    assert parse_age("50") == Age(value=50, unit="years")
    assert parse_age("22-month") == Age(value=22, unit="months")
    assert parse_age(None) is None


def test_parse_age_rejects_unknown_format():
    with pytest.raises(ValueError, match="unrecognized age format"):
        parse_age("6 weeks")


# ---------- load_split ----------

def data_row(encounter_id="D2N901", dataset="aci"):
    return {
        "dataset": dataset,
        "encounter_id": encounter_id,
        "dialogue": "[doctor] how are you\n[patient] fine",
        "note": "CHIEF COMPLAINT\n\nRoutine checkup.",
    }


def meta_row(encounter_id="D2N901", dataset="aci", age="22-month"):
    return {
        "dataset": dataset,
        "encounter_id": encounter_id,
        "id": "TEST01",
        "doctor_name": None,
        "patient_gender": "female",
        "patient_age": age,
        "patient_firstname": "Testfirst",
        "patient_familyname": "Testlast",
        "cc": "routine checkup",
        "2nd_complaints": None,
    }


def write_split(directory: Path, data_rows: list[dict], meta_rows: list[dict]) -> None:
    pd.DataFrame(data_rows).to_csv(directory / "fake.csv", index=False)
    pd.DataFrame(meta_rows).to_csv(directory / "fake_metadata.csv", index=False)


def test_load_split_returns_validated_encounters(tmp_path):
    write_split(tmp_path, [data_row()], [meta_row()])
    [encounter] = load_split(tmp_path, "fake")
    assert encounter.subset == "aci"
    assert encounter.source_id == "TEST01"
    assert encounter.patient_age == Age(value=22, unit="months")
    assert encounter.secondary_complaints is None


def test_load_split_drops_name_fields(tmp_path):
    write_split(tmp_path, [data_row()], [meta_row()])
    [encounter] = load_split(tmp_path, "fake")
    fields = encounter.model_dump()
    assert "patient_firstname" not in fields
    assert "patient_familyname" not in fields
    assert "doctor_name" not in fields


def test_load_split_fails_on_unmatched_ids(tmp_path):
    write_split(tmp_path, [data_row("D2N901")], [meta_row("D2N902")])
    with pytest.raises(ValueError, match="matched"):
        load_split(tmp_path, "fake")


def test_load_split_fails_on_subset_disagreement(tmp_path):
    write_split(tmp_path, [data_row(dataset="aci")], [meta_row(dataset="virtscribe")])
    with pytest.raises(ValueError, match="matched"):
        load_split(tmp_path, "fake")


def test_load_split_names_the_bad_encounter(tmp_path):
    write_split(tmp_path, [data_row()], [meta_row(age="6 weeks")])
    with pytest.raises(ValueError, match="D2N901"):
        load_split(tmp_path, "fake")