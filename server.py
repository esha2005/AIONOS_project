from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import uvicorn

from services.pdf_loadder import extract_text_from_pdf
from graph.workflow import recruitment_graph
from services.database import save_evaluation, fetch_all_evaluations
from services.report import generate_text_report

app = FastAPI(
    title="AIONOS AI HR Recruitment Agent API",
    description="Agentic AI REST Backend for Resume Screening, Candidate Ranking & Evaluation",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EvaluationRequest(BaseModel):
    resume_text: str
    job_description: str
    job_title: Optional[str] = "Engineering Role"
    api_key: str
    provider: Optional[str] = "openai"

@app.get("/")
def health_check():
    return {
        "status": "online",
        "service": "AIONOS Agentic AI HR Recruitment Engine",
        "version": "2.0.0"
    }

@app.post("/api/v1/evaluate")
def evaluate_candidate(req: EvaluationRequest):
    if not req.api_key:
        raise HTTPException(status_code=400, detail="API Key is required.")
    
    if req.provider == "gemini":
        os.environ["GOOGLE_API_KEY"] = req.api_key
    else:
        os.environ["OPENAI_API_KEY"] = req.api_key
        
    initial_state = {
        "resume_text": req.resume_text,
        "job_description": req.job_description,
        "candidate_name": "",
        "candidate_email": "",
        "candidate_phone": "",
        "education": "",
        "experience": "",
        "extracted_skills": [],
        "screening_result": "",
        "matched_skills": [],
        "missing_skills": [],
        "match_score": 0.0,
        "easy_questions": [],
        "intermediate_questions": [],
        "advanced_questions": [],
        "strengths": [],
        "weaknesses": [],
        "recommendation": "",
        "final_summary": "",
        "errors": []
    }
    
    try:
        final_state = recruitment_graph.invoke(initial_state)
        save_evaluation(
            candidate_name=final_state.get("candidate_name"),
            candidate_email=final_state.get("candidate_email"),
            job_title=req.job_title,
            match_score=final_state.get("match_score"),
            recommendation=final_state.get("recommendation"),
            evaluation_dict=final_state
        )
        return {"status": "success", "data": final_state}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/evaluations")
def get_evaluations():
    records = fetch_all_evaluations()
    return {"status": "success", "count": len(records), "data": records}

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
