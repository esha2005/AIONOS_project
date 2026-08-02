"""
models/summary.py
"""

from typing import List
from pydantic import BaseModel, Field


class CandidateSummary(BaseModel):

    strengths: List[str] = Field(
        default_factory=list,
        description="Candidate strengths"
    )

    weaknesses: List[str] = Field(
        default_factory=list,
        description="Candidate weaknesses"
    )

    recommendation: str = Field(
        default="",
        description="Final recommendation"
    )

    final_summary: str = Field(
        default="",
        description="Overall HR summary"
    )