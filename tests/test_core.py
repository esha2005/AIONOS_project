import unittest
from graph.state import RecruitmentState
from services.database import save_evaluation, fetch_all_evaluations

class TestCoreFunctions(unittest.TestCase):

    def test_recruitment_state_structure(self):
        state: RecruitmentState = {
            "resume_text": "Sample text",
            "job_description": "Sample JD",
            "candidate_name": "Test Candidate",
            "candidate_email": "test@example.com",
            "candidate_phone": "1234567890",
            "education": "B.Tech",
            "experience": "2 Years",
            "extracted_skills": ["Python", "FastAPI"],
            "screening_result": "Good match",
            "matched_skills": ["Python"],
            "missing_skills": ["Docker"],
            "match_score": 85.0,
            "easy_questions": ["What is Python?"],
            "intermediate_questions": ["Explain FastAPI dependency injection"],
            "advanced_questions": ["Design high-throughput async queue"],
            "strengths": ["Strong backend skills"],
            "weaknesses": ["Missing containerization experience"],
            "recommendation": "Hire",
            "final_summary": "Strong candidate for full-stack role.",
            "errors": []
        }
        self.assertEqual(state["match_score"], 85.0)
        self.assertIn("Python", state["matched_skills"])

    def test_database_persistence(self):
        save_evaluation("John Doe", "john@example.com", "AI Intern", 90.0, "Hire", {"summary": "Great"})
        records = fetch_all_evaluations()
        self.assertGreater(len(records), 0)
        self.assertEqual(records[0][1], "John Doe")

if __name__ == "__main__":
    unittest.main()
