"""
Interview Question Agent
"""

from langchain_core.prompts import ChatPromptTemplate

from services.llm import LLMService
from models.interview import InterviewQuestions
from prompts.prompts import INTERVIEW_PROMPT
from graph.state import RecruitmentState


llm = LLMService.get_llm()

structured_llm = llm.with_structured_output(
    InterviewQuestions
)


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


def interview_agent(state: RecruitmentState):

    result = chain.invoke(
        {
            "job_description": state["job_description"],
            "experience": state["experience"],
            "skills": ", ".join(state["matched_skills"]),
            "missing_skills": ", ".join(state["missing_skills"]),
        }
    )

    state["easy_questions"] = result.easy
    state["intermediate_questions"] = result.intermediate
    state["advanced_questions"] = result.advanced

    return state