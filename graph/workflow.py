"""
graph/workflow.py

Sequential LangGraph workflow for the
AI HR Recruitment Assistant.
"""

from langgraph.graph import StateGraph, START, END

from graph.state import RecruitmentState

from agents.resume_parser import resume_parser_agent
from agents.screening_agent import screening_agent
from agents.skill_matcher import skill_matcher_agent
from agents.interview_agent import interview_agent
from agents.summary_agent import summary_agent


# Create Graph
workflow = StateGraph(RecruitmentState)

# Add Nodes
workflow.add_node("resume_parser", resume_parser_agent)
workflow.add_node("screening", screening_agent)
workflow.add_node("skill_matcher", skill_matcher_agent)
workflow.add_node("interview", interview_agent)
workflow.add_node("summary", summary_agent)

# Connect Nodes
workflow.add_edge(START, "resume_parser")
workflow.add_edge("resume_parser", "screening")
workflow.add_edge("screening", "skill_matcher")
workflow.add_edge("skill_matcher", "interview")
workflow.add_edge("interview", "summary")
workflow.add_edge("summary", END)

# Compile Graph
recruitment_graph = workflow.compile()