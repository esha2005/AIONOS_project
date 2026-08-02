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


def skill_matcher_agent(state: RecruitmentState):

    result = chain.invoke(
        {
            "job_description": state["job_description"],
            "skills": ", ".join(state["extracted_skills"]),
        }
    )

    state["matched_skills"] = result.matched_skills
    state["missing_skills"] = result.missing_skills
    state["match_score"] = result.match_score

    return state