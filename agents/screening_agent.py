"""
HR Screening Agent

Compares the parsed resume with the
job description and produces a screening report.
"""

from langchain_core.prompts import ChatPromptTemplate

from services.llm import LLMService
from prompts.prompts import SCREENING_PROMPT
from graph.state import RecruitmentState

def _safe_str(val, default=""):
    if val is None:
        return default
    if isinstance(val, list):
        res = ", ".join(str(x) for x in val if x is not None).strip()
        return res if res else default
    res = str(val).strip()
    return res if res else default

def screening_agent(state: RecruitmentState):
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

    skills_list = state.get("extracted_skills", []) or []

    response = chain.invoke(
        {
            "job_description": _safe_str(state.get("job_description"), "N/A"),
            "candidate_name": _safe_str(state.get("candidate_name"), "Candidate"),
            "education": _safe_str(state.get("education"), "Not specified"),
            "experience": _safe_str(state.get("experience"), "Not specified"),
            "skills": _safe_str(skills_list, "None listed"),
        }
    )

    res_content = getattr(response, "content", "")
    state["screening_result"] = _safe_str(res_content, "Screening assessment completed.")
    return state