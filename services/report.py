import json
from typing import Dict, Any

def generate_text_report(candidate_data: Dict[str, Any]) -> str:
    name = candidate_data.get("candidate_name", "Candidate")
    email = candidate_data.get("candidate_email", "N/A")
    score = candidate_data.get("match_score", 0.0)
    rec = candidate_data.get("recommendation", "N/A")
    
    report = []
    report.append(f"==================================================")
    report.append(f"AI HR RECRUITMENT ASSESSMENT REPORT")
    report.append(f"Candidate Name : {name}")
    report.append(f"Email          : {email}")
    report.append(f"Overall Match  : {score}%")
    report.append(f"Recommendation : {rec}")
    report.append(f"==================================================\n")
    
    report.append("1. EXECUTIVE SUMMARY")
    report.append("--------------------")
    report.append(candidate_data.get("final_summary", "N/A"))
    report.append("\n2. STRENGTHS & WEAKNESSES")
    report.append("-------------------------")
    report.append("Strengths:")
    for s in candidate_data.get("strengths", []):
        report.append(f"  - {s}")
    report.append("Weaknesses:")
    for w in candidate_data.get("weaknesses", []):
        report.append(f"  - {w}")

    report.append("\n3. SKILL BREAKDOWN")
    report.append("------------------")
    report.append(f"Matched Skills : {', '.join(candidate_data.get('matched_skills', []))}")
    report.append(f"Missing Skills : {', '.join(candidate_data.get('missing_skills', []))}")

    report.append("\n4. TAILORED INTERVIEW QUESTIONS")
    report.append("-------------------------------")
    report.append("Easy Level:")
    for q in candidate_data.get("easy_questions", []):
        report.append(f"  - {q}")
    report.append("Intermediate Level:")
    for q in candidate_data.get("intermediate_questions", []):
        report.append(f"  - {q}")
    report.append("Advanced Level:")
    for q in candidate_data.get("advanced_questions", []):
        report.append(f"  - {q}")
        
    return "\n".join(report)
