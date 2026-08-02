"""
models/interview.py
"""

from typing import List
from pydantic import BaseModel, Field


class InterviewQuestions(BaseModel):
    easy: List[str] = Field(
        default_factory=list,
        description="Easy interview questions"
    )

    intermediate: List[str] = Field(
        default_factory=list,
        description="Intermediate interview questions"
    )

    advanced: List[str] = Field(
        default_factory=list,
        description="Advanced interview questions"
    )