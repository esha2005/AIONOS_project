"""
Candidate Summary Agent
"""

from langchain_core.prompts import ChatPromptTemplate

from services.llm import LLMService
from models.summary import CandidateSummary
from prompts.prompts import SUMMARY_PROMPT
from graph.state import RecruitmentState

def _safe_str(val, default=""):
    if val is None:
        return default
    if isinstance(val, list):
        res = "\n".join(str(x) for x in val if x is not None).strip()
        return res if res else default
    res = str(val).strip()
    return res if res else default

def summary_agent(state: RecruitmentState):
    llm = LLMService.get_llm()
    structured_llm = llm.with_structured_output(CandidateSummary)
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

    matched = state.get("matched_skills", []) or []
    missing = state.get("missing_skills", []) or []

    result = chain.invoke(
        {
            "name": _safe_str(state.get("candidate_name"), "Candidate"),
            "education": _safe_str(state.get("education"), "Not specified"),
            "experience": _safe_str(state.get("experience"), "Not specified"),
            "matched_skills": ", ".join(str(x) for x in matched) if matched else "None listed",
            "missing_skills": ", ".join(str(x) for x in missing) if missing else "None listed",
            "match_score": state.get("match_score", 0.0),
            "screening": _safe_str(state.get("screening_result"), "Screening complete"),
        }
    )

    state["strengths"] = getattr(result, "strengths", []) or []
    state["weaknesses"] = getattr(result, "weaknesses", []) or []
    state["recommendation"] = getattr(result, "recommendation", "") or "Hold"
    state["final_summary"] = getattr(result, "final_summary", "") or "Evaluation completed."

    return state