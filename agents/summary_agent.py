"""
Candidate Summary Agent
"""

from langchain_core.prompts import ChatPromptTemplate

from services.llm import LLMService
from models.summary import CandidateSummary
from prompts.prompts import SUMMARY_PROMPT
from graph.state import RecruitmentState

llm = LLMService.get_llm()

structured_llm = llm.with_structured_output(
    CandidateSummary
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SUMMARY_PROMPT),
        (
            "human",
            """
Candidate Name

{name}

Education

{education}

Experience

{experience}

Matched Skills

{matched_skills}

Missing Skills

{missing_skills}

Match Score

{match_score}

Screening Result

{screening}
"""
        ),
    ]
)

chain = prompt | structured_llm


def summary_agent(state: RecruitmentState):

    result = chain.invoke(
        {
            "name": state["candidate_name"],
            "education": state["education"],
            "experience": state["experience"],
            "matched_skills": ", ".join(state["matched_skills"]),
            "missing_skills": ", ".join(state["missing_skills"]),
            "match_score": state["match_score"],
            "screening": state["screening_result"],
        }
    )

    state["strengths"] = result.strengths
    state["weaknesses"] = result.weaknesses
    state["recommendation"] = result.recommendation
    state["final_summary"] = result.final_summary

    return state