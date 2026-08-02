"""
Pydantic model returned by the Resume Parser Agent.
"""

from typing import List
from pydantic import BaseModel, Field


class Resume(BaseModel):

    candidate_name: str = Field(
        default="",
        description="Candidate full name"
    )

    candidate_email: str = Field(
        default="",
        description="Candidate email"
    )

    candidate_phone: str = Field(
        default="",
        description="Candidate phone"
    )

    education: str = Field(
        default="",
        description="Highest education"
    )

    experience: str = Field(
        default="",
        description="Professional experience"
    )

    extracted_skills: List[str] = Field(
        default_factory=list,
        description="Candidate skills"
    )