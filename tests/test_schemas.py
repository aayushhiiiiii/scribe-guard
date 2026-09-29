import pytest
from pydantic import ValidationError

from scribe_guard.schemas import Flag


def test_flag_accepts_valid_error_type():
    flag = Flag(
        error_type="omission",
        explanation="Penicillin allergy mentioned in transcript but missing from note.",
    )
    assert flag.error_type == "omission"


def test_flag_rejects_unknown_error_type():
    with pytest.raises(ValidationError):
        Flag(error_type="typo", explanation="Not a real error category.")