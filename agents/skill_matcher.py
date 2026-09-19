"""
agents/skill_matcher.py

Compares resume skills with job description
and returns structured skill matching results.
"""

from langchain_core.prompts import ChatPromptTemplate

from services.llm import LLMService
from graph.state import RecruitmentState
from prompts.prompts import SKILL_MATCH_PROMPT
from models.skill_match import SkillMatch


def skill_matcher_agent(state: RecruitmentState):
    llm = LLMService.get_llm()
    structured_llm = llm.with_structured_output(SkillMatch)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SKILL_MATCH_PROMPT),
            (
                "human",
                """
Job Description

{job_description}

Candidate Skills

{skills}
                """
            ),
        ]
    )
    chain = prompt | structured_llm

    skills_list = state.get("extracted_skills", []) or []
    skills_str = ", ".join(skills_list) if skills_list else "None listed"

    result = chain.invoke(
        {
            "job_description": (state.get("job_description", "") or "").strip() or "N/A",
            "skills": skills_str,
        }
    )

    state["matched_skills"] = getattr(result, "matched_skills", []) or []
    state["missing_skills"] = getattr(result, "missing_skills", []) or []
    score_val = getattr(result, "match_score", 0.0)
    try:
        state["match_score"] = float(score_val)
    except (ValueError, TypeError):
        state["match_score"] = 0.0

    return state