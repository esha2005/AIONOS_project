"""
models/skill_match.py

Pydantic model for the Skill Matching Agent.
"""

from typing import List
from pydantic import BaseModel, Field


class SkillMatch(BaseModel):
    matched_skills: List[str] = Field(
        default_factory=list,
        description="Skills found in both the resume and job description."
    )

    missing_skills: List[str] = Field(
        default_factory=list,
        description="Required skills missing from the resume."
    )

    match_score: float = Field(
        default=0,
        description="Overall skill match percentage (0-100)."
    )