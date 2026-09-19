# 💼 AIONOS Agentic AI HR Recruitment Platform

> **AIONOS Agentic AI Factory Internship Submission**  
> Built to automate candidate screening, skill matching, interview generation, batch candidate ranking, and recruitment audit logs using multi-agent state graph orchestration.

---

## 🚀 Key Features

1. **Multi-Agent Orchestration (LangGraph)**:
   - **Resume Parser Agent**: Extracts structured candidate entities from raw PDF files.
   - **HR Screening Agent**: Audits match quality against specific Job Description requirements.
   - **Skill Matcher Agent**: Generates matched vs missing skills and calculates overall fit score.
   - **Interview Generator Agent**: Produces difficulty-tiered technical interview questions (Easy, Intermediate, Advanced).
   - **Summary Agent**: Synthesizes final hiring recommendations (`Hire`, `Technical Interview`, `Hold`, `Reject`).

2. **Full-Stack Architecture**:
   - **Interactive Web App (`app.py`)**: Glassmorphic UI supporting Single Resume Audit, Batch Candidate Leaderboards, and Evaluation Logs.
   - **REST API Backend (`server.py`)**: High-performance FastAPI endpoints for third-party ATS integration (`/api/v1/evaluate`, `/api/v1/evaluations`).
   - **Database Persistence (`services/database.py`)**: SQLite storage for tracking candidate history.
   - **Multi-Model LLM Support**: Supports both **OpenAI** (`gpt-4o`/`gpt-4o-mini`) and **Google Gemini** (`gemini-1.5-flash`).

3. **Report Generation & Leaderboards**:
   - **Batch Candidate Leaderboard**: Compares and ranks multiple resumes against a single Job Description.
   - **Exportable Assessment Reports**: Generates downloadable text reports for HR records.

---

## 🛠️ Quick Start & Installation

### 1. Local Setup
```bash
# Clone the repository (if not already local)
git clone https://github.com/kiran-hayat/AI-HR-Recruitment-Agent.git
cd AI-HR-Recruitment-Agent

# Install dependencies
pip install -r requirements.txt
```

### 2. Running the Interactive UI (Streamlit)
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`. Choose your LLM Provider (OpenAI or Gemini), input your API Key, and upload candidate resumes!

### 3. Running the Production REST API (FastAPI)
```bash
python server.py
# or using uvicorn
uvicorn server:app --reload --port 8000
```
Swagger UI docs available at `http://localhost:8000/docs`.

---

## 🧪 Testing

Run the automated test suite:
```bash
python -m unittest tests/test_core.py
```

---

## 🐳 Docker Deployment

```bash
docker-compose up --build
```
- **Streamlit App**: `http://localhost:8501`
- **FastAPI Endpoints**: `http://localhost:8000`

---

## 📂 Architecture Overview

```
├── app.py                 # Streamlit Glassmorphic Frontend
├── server.py              # FastAPI REST Endpoints
├── graph/
│   ├── state.py           # LangGraph State Definition
│   └── workflow.py        # Multi-Agent Sequential & Dynamic Graph
├── agents/                # LLM Sub-agents (Parser, Screening, Skill Matcher, Interview, Summary)
├── services/              # LLM service, Database persistence, PDF loader, Report generator
├── tests/                 # Unit test suite
├── Dockerfile             # Container configuration
└── docker-compose.yml     # Container orchestration
```
