"""Data structures shared across the project."""

from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class Flag(BaseModel):
    """One suspected error found in an AI-generated clinical note."""

    error_type: Literal["hallucination", "omission"]
    explanation: str
    note_text: str | None = None
    transcript_evidence: str | None = None


Subset = Literal["aci", "virtassist", "virtscribe"]

class Encounter(BaseModel):
    """One ACI-BENCH encounter: dialogue, reference note, and selected metadata."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    encounter_id: str = Field(pattern=r"^D2N\d{3}$")
    source_id: str = Field(min_length=1)
    subset: Subset
    dialogue: str = Field(min_length=1)
    note: str = Field(min_length=1)
    chief_complaint: str = Field(min_length=1)
    secondary_complaints: str | None = None
    patient_age: int | None = Field(default=None, ge=0, le=120)
    patient_gender: str | None = None