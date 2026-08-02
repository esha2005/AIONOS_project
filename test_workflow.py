from graph.workflow import recruitment_graph

state = {

    "resume_text": """
John Smith

Email: john@gmail.com

Phone: +92-300-1234567

BS Computer Science

Experience

3 Years as Data Scientist

Skills

Python
SQL
Machine Learning
TensorFlow
Pandas
Git
""",

    "job_description": """
We are hiring a Data Scientist.

Required Skills

Python
SQL
Machine Learning
TensorFlow
Docker
AWS
Git
""",

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
    "final_summary": "",

    "errors": []
}

result = recruitment_graph.invoke(state)

print("=" * 60)
print("Candidate")
print(result["candidate_name"])

print("=" * 60)
print("Match Score")
print(result["match_score"])

print("=" * 60)
print("Recommendation")
print(result["recommendation"])

print("=" * 60)
print("Summary")
print(result["final_summary"])