"""
Interview Question Agent
"""

from langchain_core.prompts import ChatPromptTemplate

from services.llm import LLMService
from models.interview import InterviewQuestions
from prompts.prompts import INTERVIEW_PROMPT
from graph.state import RecruitmentState


def interview_agent(state: RecruitmentState):
    llm = LLMService.get_llm()
    structured_llm = llm.with_structured_output(InterviewQuestions)
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", INTERVIEW_PROMPT),
            (
                "human",
                """
Job Description

{job_description}

Experience

{experience}

Skills

{skills}

Missing Skills

{missing_skills}
"""
            ),
        ]
    )
    chain = prompt | structured_llm

    matched = state.get("matched_skills", []) or []
    missing = state.get("missing_skills", []) or []

    result = chain.invoke(
        {
            "job_description": (state.get("job_description", "") or "").strip() or "N/A",
            "experience": (state.get("experience", "") or "").strip() or "Not specified",
            "skills": ", ".join(matched) if matched else "None listed",
            "missing_skills": ", ".join(missing) if missing else "None listed",
        }
    )

    state["easy_questions"] = getattr(result, "easy", []) or []
    state["intermediate_questions"] = getattr(result, "intermediate", []) or []
    state["advanced_questions"] = getattr(result, "advanced", []) or []

    return state