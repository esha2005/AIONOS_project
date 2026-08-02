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


llm = LLMService.get_llm()

structured_llm = llm.with_structured_output(Resume)


prompt = ChatPromptTemplate.from_messages(
    [
        ("system", RESUME_PARSER_PROMPT),
    ]
)


def resume_parser_agent(
    state: RecruitmentState,
):

    chain = prompt | structured_llm

    result = chain.invoke(
        {
            "resume": state["resume_text"]
        }
    )

    state["candidate_name"] = result.candidate_name

    state["candidate_email"] = result.candidate_email

    state["candidate_phone"] = result.candidate_phone

    state["education"] = result.education

    state["experience"] = result.experience

    state["extracted_skills"] = result.extracted_skills

    return state