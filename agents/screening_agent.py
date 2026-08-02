"""
HR Screening Agent

Compares the parsed resume with the
job description and produces a screening report.
"""

from langchain_core.prompts import ChatPromptTemplate

from services.llm import LLMService
from prompts.prompts import SCREENING_PROMPT
from graph.state import RecruitmentState

llm = LLMService.get_llm()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SCREENING_PROMPT),
        (
            "human",
            """
Job Description:
{job_description}

Resume

Name:
{candidate_name}

Education:
{education}

Experience:
{experience}

Skills:
{skills}
            """,
        ),
    ]
)

chain = prompt | llm


def screening_agent(state: RecruitmentState):

    response = chain.invoke(
        {
            "job_description": state["job_description"],
            "candidate_name": state["candidate_name"],
            "education": state["education"],
            "experience": state["experience"],
            "skills": ", ".join(state["extracted_skills"]),
        }
    )

    state["screening_result"] = response.content

    return state