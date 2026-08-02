from agents.resume_parser import resume_parser_agent

state = {
    "resume_text": """
John Smith

Email: john@gmail.com

Phone: +92 3001234567

BS Computer Science

Skills

Python
SQL
Machine Learning
TensorFlow
Pandas

Experience

3 years as Data Scientist
""",

    "job_description": "",

    "candidate_name": None,
    "candidate_email": None,
    "candidate_phone": None,

    "education": "",
    "experience": "",

    "extracted_skills": [],

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

result = resume_parser_agent(state)

print(result)