from graph.state import RecruitmentState

state: RecruitmentState = {
    "resume_text": "Python ML SQL",
    "job_description": "Need Python Data Scientist",

    "candidate_name": None,
    "candidate_email": None,
    "candidate_phone": None,

    "extracted_skills": [],
    "experience": "",
    "education": "",

    "screening_result": "",

    "matched_skills": [],
    "missing_skills": [],
    "match_score": 0,

    "easy_questions": [],
    "intermediate_questions": [],
    "advanced_questions": [],

    "strengths": [],
    "weaknesses": [],
    "recommendation": "",

    "errors": []
}

print(state)