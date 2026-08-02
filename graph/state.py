from typing import TypedDict, List, Optional


class RecruitmentState(TypedDict):

    # Inputs
    resume_text: str
    job_description: str

    # Candidate Info
    candidate_name: Optional[str]
    candidate_email: Optional[str]
    candidate_phone: Optional[str]

    education: str
    experience: str

    extracted_skills: List[str]

    # Screening
    screening_result: str

    # Skill Matching
    matched_skills: List[str]
    missing_skills: List[str]
    match_score: float

    # Interview
    easy_questions: List[str]
    intermediate_questions: List[str]
    advanced_questions: List[str]

    # Summary
    strengths: List[str]
    weaknesses: List[str]
    recommendation: str
    final_summary: str

    # Errors
    errors: List[str]