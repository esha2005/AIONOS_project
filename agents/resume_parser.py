"""
Resume Parser Agent

Extracts structured information from
the uploaded resume.
"""

from langchain_core.prompts import ChatPromptTemplate

from services.llm import LLMService
from prompts.prompts import RESUME_PARSER_PROMPT
from graph.state import RecruitmentState
from models.resume import Resume


def resume_parser_agent(
    state: RecruitmentState,
):
    llm = LLMService.get_llm()
    structured_llm = llm.with_structured_output(Resume)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert HR Resume Parsing Assistant. Extract candidate information structured accurately."),
        ("human", "Extract info from resume:\n{resume}")
    ])
    chain = prompt | structured_llm

    resume_raw = state.get("resume_text", "") or ""
    resume_content = resume_raw.strip() or "No resume text provided."

    result = chain.invoke(
        {
            "resume": resume_content
        }
    )

    state["candidate_name"] = (getattr(result, "candidate_name", "") or "").strip() or "Candidate"
    state["candidate_email"] = (getattr(result, "candidate_email", "") or "").strip() or "N/A"
    state["candidate_phone"] = (getattr(result, "candidate_phone", "") or "").strip() or "N/A"
    state["education"] = (getattr(result, "education", "") or "").strip() or "Not specified"
    state["experience"] = (getattr(result, "experience", "") or "").strip() or "Not specified"
    state["extracted_skills"] = getattr(result, "extracted_skills", []) or []

    return state