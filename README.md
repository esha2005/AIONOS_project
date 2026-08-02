# 🤖 AI HR Recruitment Assistant

An **Agentic AI Recruitment System** built with **LangGraph, LangChain, OpenAI, and Streamlit** that automates the early stages of the recruitment process.

Instead of using a single prompt, this application follows a **Sequential Agent Workflow** where multiple AI agents collaborate to analyze a candidate's resume, compare it with a job description, generate interview questions, and provide a hiring recommendation.

---

# Project Objective

Recruiters often spend a significant amount of time reviewing resumes, comparing candidates against job requirements, and preparing interviews.

This project demonstrates how an Agentic AI workflow can automate these repetitive tasks while keeping the final hiring decision with the HR team.

The system is designed as a portfolio project to showcase modern AI engineering concepts such as:

* LangGraph Workflows
* Multi-Agent Systems
* Large Language Models (LLMs)
* Structured Outputs
* Prompt Engineering
* State Management
* Streamlit Applications

---

# Tech Stack

| Technology          | Purpose                |
| ------------------- | ---------------------- |
| Python              | Backend                |
| Streamlit           | Web Interface          |
| LangGraph           | Workflow Orchestration |
| LangChain           | LLM Framework          |
| OpenAI GPT-4.1 Mini | Language Model         |
| Pydantic            | Structured Outputs     |
| PyPDF               | Resume Text Extraction |
| Python-dotenv       | Environment Variables  |

---

# Project Architecture

```text
                    User

                     │

                     ▼

             Streamlit Interface

                     │

                     ▼

          Upload Resume (PDF)

                     │

                     ▼

           Paste Job Description

                     │

                     ▼

            LangGraph Workflow

                     │

     ┌───────────────┴────────────────┐

                     ▼

          Resume Parser Agent

                     │

                     ▼

         HR Screening Agent

                     │

                     ▼

          Skill Matching Agent

                     │

                     ▼

     Interview Question Agent

                     │

                     ▼

        Candidate Summary Agent

                     │

                     ▼

          Final Hiring Decision
```

---

# Sequential Workflow

This project uses a **Sequential Workflow**, meaning every agent waits for the previous agent to complete before executing.

```text
START

↓

Resume Parser

↓

Resume Screening

↓

Skill Matching

↓

Interview Question Generator

↓

Candidate Summary

↓

END
```

Each agent updates a shared state object, and the next agent uses the updated information.

---

# Shared State (LangGraph State)

The workflow maintains a shared state throughout execution.

Typical fields include:

```python
resume_text

job_description

candidate_name

candidate_email

candidate_phone

education

experience

extracted_skills

screening_result

matched_skills

missing_skills

match_score

easy_questions

intermediate_questions

advanced_questions

strengths

weaknesses

recommendation

final_summary

errors
```

Every node receives this state, modifies it, and passes it to the next node.

---

# Agent 1 — Resume Parser

## Purpose

Extract structured information from an uploaded resume.

## Input

* Resume PDF

## Processing

* Extract PDF text
* Send text to GPT
* Convert response into structured data

## Output

* Candidate Name
* Email
* Phone
* Education
* Experience
* Skills

Example

```text
John Smith

Email:
john@gmail.com

Phone:
+92-300-1234567

Education:
BS Computer Science

Skills:
Python
SQL
TensorFlow
Machine Learning
```

---

# Agent 2 — Resume Screening

## Purpose

Evaluate whether the candidate generally fits the job.

The agent analyzes

* Experience
* Education
* Technical Skills
* Resume Quality

Example Output

```text
Overall Suitability:
Good

Strengths

• Relevant experience

• Strong Python knowledge

Weaknesses

• AWS not mentioned

Recommendation

Proceed to skill matching
```

---

# Agent 3 — Skill Matching

## Purpose

Compare candidate skills against the required skills from the job description.

Example

Job Description

```text
Python

SQL

Docker

AWS

TensorFlow
```

Candidate

```text
Python

SQL

TensorFlow
```

Output

```text
Matched Skills

Python

SQL

TensorFlow

Missing Skills

Docker

AWS

Match Score

60%
```

---

# Agent 4 — Interview Question Generator

## Purpose

Generate personalized interview questions based on

* Experience
* Skills
* Missing Skills
* Job Description

Questions are divided into three categories.

Easy

```text
What is Machine Learning?

Explain SQL JOIN.
```

Intermediate

```text
How does Random Forest work?

Explain Cross Validation.
```

Advanced

```text
Design an end-to-end recommendation system.

How would you deploy a transformer model?
```

---

# Agent 5 — Candidate Summary

The final agent combines outputs from every previous agent.

It generates

* Candidate Strengths
* Candidate Weaknesses
* Final Summary
* Hiring Recommendation

Possible recommendations

* Hire
* Technical Interview
* Hold
* Reject

Example

```text
Recommendation

Technical Interview

Summary

The candidate has strong experience in Python and Machine Learning with a good educational background. While cloud technologies such as Docker and AWS are missing, the overall profile is suitable for further technical evaluation.
```

---

# LangGraph Workflow

The workflow follows this execution order.

```text
START

↓

Resume Parser

↓

Screening

↓

Skill Matcher

↓

Interview Generator

↓

Summary

↓

END
```

Each node updates the shared state.

---

# Folder Structure

```text
AI-HR-Recruitment-Agent/

│

├── agents/

│ ├── resume_parser.py

│ ├── screening_agent.py

│ ├── skill_matcher.py

│ ├── interview_agent.py

│ └── summary_agent.py

│

├── graph/

│ ├── workflow.py

│ └── state.py

│

├── models/

│ ├── resume.py

│ ├── skill_match.py

│ ├── interview.py

│ └── summary.py

│

├── prompts/

│ └── prompts.py

│

├── services/

│ ├── llm.py

│ └── pdf_loader.py

│

├── config/

│ └── settings.py

│

├── app.py

├── requirements.txt

├── README.md

└── .env
```

---

# Expected User Flow

1. Open the Streamlit application.
2. Upload a resume in PDF format.
3. Paste the job description.
4. Click **Start Recruitment Workflow**.
5. The workflow executes each agent sequentially.
6. View the candidate analysis, skill match, interview questions, and hiring recommendation.

---

# Possible Future Improvements

This project can be extended with several advanced features:

* Support for multiple resumes at once.
* Resume ranking and candidate leaderboard.
* OCR support for scanned resumes.
* Resume embeddings stored in a vector database.
* RAG to answer HR questions based on company policies.
* Recruiter feedback loop for improving recommendations.
* Email shortlisted candidates automatically.
* Calendar integration to schedule interviews.
* Dashboard with recruitment analytics.
* Support for multiple LLM providers (OpenAI, Gemini, Azure OpenAI, Anthropic).

---

# Learning Outcomes

This project demonstrates practical experience with:

* Agentic AI workflows.
* Sequential workflow design.
* LangGraph state management.
* Prompt engineering.
* Structured outputs with Pydantic.
* LangChain integration.
* Building AI-powered business applications.
* Streamlit interface development.
* GitHub project organization.

---

# License

This project is intended for educational and portfolio purposes. Feel free to fork, extend, and adapt it for learning or internal business prototypes.
