import pytest
from pydantic import ValidationError

from scribe_guard.schemas import Encounter, Flag


def test_flag_accepts_valid_error_type():
    flag = Flag(
        error_type="omission",
        explanation="Penicillin allergy mentioned in transcript but missing from note.",
    )
    assert flag.error_type == "omission"


def test_flag_rejects_unknown_error_type():
    with pytest.raises(ValidationError):
        Flag(error_type="typo", explanation="Not a real error category.")

def make_encounter_data(**overrides):
    """Return valid Encounter fields; a test can override any field."""
    data = {
        "encounter_id": "D2N999",
        "source_id": "TEST001",
        "subset": "aci",
        "dialogue": "[doctor] how is your knee\n[patient] it hurts",
        "note": "CHIEF COMPLAINT\n\nKnee pain.",
        "chief_complaint": "knee pain",
    }
    data.update(overrides)
    return data


def test_encounter_accepts_valid_data():
    encounter = Encounter(**make_encounter_data())
    assert encounter.subset == "aci"
    assert encounter.patient_age is None


def test_encounter_converts_whole_float_age_to_int():
    encounter = Encounter(**make_encounter_data(patient_age=45.0))
    assert encounter.patient_age == 45
    assert isinstance(encounter.patient_age, int)


def test_encounter_rejects_unknown_subset():
    with pytest.raises(ValidationError):
        Encounter(**make_encounter_data(subset="vitrassist"))


def test_encounter_rejects_extra_field():
    with pytest.raises(ValidationError):
        Encounter(**make_encounter_data(dataset="aci"))


def test_encounter_rejects_malformed_id():
    with pytest.raises(ValidationError):
        Encounter(**make_encounter_data(encounter_id="D2N1"))


def test_encounter_rejects_empty_dialogue():
    with pytest.raises(ValidationError):
        Encounter(**make_encounter_data(dialogue=""))


def test_encounter_rejects_impossible_age():
    with pytest.raises(ValidationError):
        Encounter(**make_encounter_data(patient_age=200))


def test_encounter_is_immutable():
    encounter = Encounter(**make_encounter_data())
    with pytest.raises(ValidationError):
        encounter.subset = "virtscribe"