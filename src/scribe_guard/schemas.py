"""Data structures shared across the project."""

from typing import Literal

from pydantic import BaseModel


class Flag(BaseModel):
    """One suspected error found in an AI-generated clinical note."""

    error_type: Literal["hallucination", "omission"]
    explanation: str
    note_text: str | None = None
    transcript_evidence: str | None = None