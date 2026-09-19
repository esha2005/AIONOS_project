import streamlit as st
import os
import json

from services.pdf_loadder import extract_text_from_pdf
from services.database import save_evaluation, fetch_all_evaluations
from services.report import generate_text_report

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AIONOS - AI HR Recruitment Platform",
    page_icon="🤖",
    layout="wide"
)

# Custom Styling
st.markdown("""
<style>
    .main {
        background-color: #0f172a;
        color: #f8fafc;
    }
    .stButton>button {
        width: 100%;
        background-color: #3b82f6;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #2563eb;
    }
    .metric-card {
        background-color: #1e293b;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #334155;
    }
</style>
""", unsafe_allow_html=True)


if "LLM_PROVIDER" not in st.session_state:
    st.session_state["LLM_PROVIDER"] = "OpenAI"
if "API_KEY" not in st.session_state:
    st.session_state["API_KEY"] = ""

# -----------------------------
# API Key Gate Screen
# -----------------------------
if not st.session_state["API_KEY"]:
    st.title("🤖 AIONOS Agentic AI HR Recruitment Platform")
    st.markdown("### 🔑 Choose AI Provider & Set API Key to Initialize Agents")

    with st.form("api_key_form"):
        provider = st.selectbox("Select LLM Provider", ["OpenAI", "Google Gemini"])
        key_input = st.text_input("API Key", type="password", placeholder="Enter key...")
        gemini_model = st.selectbox(
            "Gemini Model (if Google Gemini selected)",
            [
                "gemini-2.0-flash",
                "gemini-3.5-flash",
                "gemini-1.5-flash",
                "gemini-1.5-pro",
            ]
        )
        submitted = st.form_submit_button("Launch HR Engine")

        if submitted:
            if key_input.strip():
                from services.llm import _get_cached_llm
                _get_cached_llm.cache_clear()

                st.session_state["LLM_PROVIDER"] = provider
                st.session_state["API_KEY"] = key_input.strip()
                st.session_state["GEMINI_MODEL_NAME"] = gemini_model
                os.environ["GEMINI_MODEL_NAME"] = gemini_model
                if provider == "OpenAI":
                    os.environ["OPENAI_API_KEY"] = key_input.strip()
                    st.session_state["OPENAI_API_KEY"] = key_input.strip()
                    os.environ["LLM_PROVIDER"] = "openai"
                else:
                    os.environ["GOOGLE_API_KEY"] = key_input.strip()
                    st.session_state["GOOGLE_API_KEY"] = key_input.strip()
                    os.environ["LLM_PROVIDER"] = "gemini"
                st.rerun()
            else:
                st.error("Please enter a valid API key.")
    st.stop()

# Safe import after API Key configuration
from graph.workflow import recruitment_graph

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.title("⚡ AIONOS AI HR Suite")
current_model = st.session_state.get("GEMINI_MODEL_NAME", "gemini-2.0-flash") if st.session_state.get("LLM_PROVIDER") == "Google Gemini" else "OpenAI"
st.sidebar.caption(f"Provider: {st.session_state['LLM_PROVIDER']} ({current_model}) ✅")

if st.sidebar.button("⚙️ Reset API Key"):
    from services.llm import _get_cached_llm
    _get_cached_llm.cache_clear()
    st.session_state["API_KEY"] = ""
    st.rerun()

app_mode = st.sidebar.radio("Navigate Module", ["Single Candidate Assessment", "Batch Leaderboard", "Evaluation Database"])

# -----------------------------
# 1. Single Candidate Assessment
# -----------------------------
if app_mode == "Single Candidate Assessment":
    st.title("👤 Single Candidate Recruitment Agent Workflow")
    st.markdown("Upload candidate resume PDF and specify target Job Description.")

    col_up, col_jd = st.columns([1, 1])

    with col_up:
        uploaded_pdf = st.file_uploader("Upload Candidate Resume (PDF)", type=["pdf"])
        resume_text = ""
        if uploaded_pdf:
            try:
                resume_text = extract_text_from_pdf(uploaded_pdf)
                if resume_text.strip():
                    st.success("Resume text extracted successfully!")
                    with st.expander("Preview Resume Text"):
                        st.text_area("Parsed Text", resume_text, height=150)
                else:
                    st.warning("⚠️ Warning: Could not extract text from this PDF. It may be scanned or image-only.")
            except Exception as e:
                st.error(f"Error reading PDF: {e}")

    with col_jd:
        job_description = st.text_area("Target Job Description", height=220, placeholder="Paste JD requirements...")

    if st.button("🚀 Run Agentic Multi-Agent Audit"):
        if not resume_text or not resume_text.strip():
            st.error("Please upload a valid resume PDF with readable text.")
        elif not job_description.strip():
            st.error("Please enter a Job Description.")
        else:
            initial_state = {
                "resume_text": resume_text,
                "job_description": job_description,
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

            step_labels = {
                "resume_parser": "📄 Step 1/5: Resume Parser — Extracting candidate profile & skills...",
                "screening": "🔍 Step 2/5: Screening Agent — Analyzing fit against job description...",
                "skill_matcher": "🎯 Step 3/5: Skill Matcher — Computing matched/missing skills & score...",
                "interview": "❓ Step 4/5: Interview Agent — Generating tailored interview questions...",
                "summary": "📝 Step 5/5: Summarizer — Producing final evaluation & recommendation...",
            }

            progress_bar = st.progress(0, text="🚀 Starting multi-agent workflow...")
            status_placeholder = st.empty()
            result = initial_state.copy()
            last_node = None

            try:
                for step in recruitment_graph.stream(initial_state):
                    for node_name, node_output in step.items():
                        if isinstance(node_output, dict):
                            result.update(node_output)
                        if node_name in step_labels and node_name != last_node:
                            last_node = node_name
                            idx = list(step_labels.keys()).index(node_name)
                            progress_bar.progress((idx + 1) / len(step_labels), text=step_labels[node_name])
                            status_placeholder.info(step_labels[node_name])
                progress_bar.progress(1.0, text="✅ Multi-Agent Workflow Completed!")
                status_placeholder.empty()
            except Exception as e:
                progress_bar.empty()
                status_placeholder.empty()
                st.error(f"Workflow execution failed: {e}")
                result = None

            if result:
                st.success("✅ Multi-Agent Workflow Completed Successfully!")
                save_evaluation(
                    candidate_name=result.get("candidate_name"),
                    candidate_email=result.get("candidate_email"),
                    job_title="Assigned Role",
                    match_score=result.get("match_score"),
                    recommendation=result.get("recommendation"),
                    evaluation_dict=result
                )

                # Results Display
                st.header("1️⃣ Candidate Profile")
                m1, m2, m3 = st.columns(3)
                m1.metric("Candidate Name", result.get("candidate_name") or "N/A")
                m2.metric("Email", result.get("candidate_email") or "N/A")
                m3.metric("Match Score", f"{result.get('match_score', 0)}%")

                st.subheader("2️⃣ Screening Audit")
                st.info(result.get("screening_result") or "N/A")

                st.subheader("3️⃣ Skill Matrix")
                sc1, sc2 = st.columns(2)
                with sc1:
                    st.write("**✅ Matched Skills**")
                    for sk in result.get("matched_skills", []):
                        st.write(f"- {sk}")
                with sc2:
                    st.write("**❌ Missing / Gap Skills**")
                    for sk in result.get("missing_skills", []):
                        st.write(f"- {sk}")

                st.subheader("4️⃣ Tailored Interview Questions")
                q1, q2, q3 = st.tabs(["Easy Questions", "Intermediate Questions", "Advanced Questions"])
                with q1:
                    for q in result.get("easy_questions", []):
                        st.write(f"- {q}")
                with q2:
                    for q in result.get("intermediate_questions", []):
                        st.write(f"- {q}")
                with q3:
                    for q in result.get("advanced_questions", []):
                        st.write(f"- {q}")

                st.subheader("5️⃣ Final Evaluation & Recommendation")
                rec = result.get("recommendation", "N/A")
                st.markdown(f"### **Recommendation:** `{rec}`")
                st.write(result.get("final_summary", ""))

                # Download Assessment Report
                report_txt = generate_text_report(result)
                st.download_button(
                    label="📥 Download Official HR Report (.txt)",
                    data=report_txt,
                    file_name=f"{result.get('candidate_name', 'Candidate')}_Evaluation.txt",
                    mime="text/plain"
                )

# -----------------------------
# 2. Batch Leaderboard
# -----------------------------
elif app_mode == "Batch Leaderboard":
    st.title("🏆 Batch Candidates Leaderboard & Ranking Engine")
    st.markdown("Upload multiple candidate resumes to compare and rank against one Job Description.")

    batch_files = st.file_uploader("Upload Multiple Resumes (PDF)", type=["pdf"], accept_multiple_files=True)
    batch_jd = st.text_area("Job Description for Batch Ranking", height=180)

    if st.button("📊 Evaluate & Rank Batch"):
        if not batch_files:
            st.error("Please upload at least one candidate PDF.")
        elif not batch_jd.strip():
            st.error("Please enter Job Description.")
        else:
            rankings = []
            progress_bar = st.progress(0, text=f"Starting batch evaluation of {len(batch_files)} candidates...")
            status_placeholder = st.empty()

            for idx, file in enumerate(batch_files):
                status_placeholder.info(f"Evaluating candidate {idx + 1}/{len(batch_files)}: {file.name}")
                try:
                    text = extract_text_from_pdf(file)
                    state = {
                        "resume_text": text,
                        "job_description": batch_jd,
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
                    res = state.copy()
                    for step in recruitment_graph.stream(state):
                        for _, node_output in step.items():
                            if isinstance(node_output, dict):
                                res.update(node_output)
                    if res and res.get("candidate_name") is not None:
                        rankings.append({
                            "Name": res.get("candidate_name") or file.name,
                            "Email": res.get("candidate_email") or "N/A",
                            "Match Score (%)": res.get("match_score", 0),
                            "Recommendation": res.get("recommendation", "N/A"),
                            "Matched Count": len(res.get("matched_skills", [])),
                            "Missing Count": len(res.get("missing_skills", []))
                        })
                except Exception as e:
                    st.warning(f"Error evaluating {file.name}: {e}")

                progress_bar.progress((idx + 1) / len(batch_files), text=f"Candidate {idx + 1}/{len(batch_files)} done: {file.name}")

            status_placeholder.empty()
            progress_bar.progress(1.0, text=f"✅ Batch evaluation complete — {len(rankings)} candidates ranked.")

            if rankings:
                rankings = sorted(rankings, key=lambda x: x["Match Score (%)"], reverse=True)
                st.subheader("🥇 Candidates Leaderboard")
                st.table(rankings)

# -----------------------------
# 3. Evaluation Database
# -----------------------------
elif app_mode == "Evaluation Database":
    st.title("🗄️ Candidate Evaluation Persistence Log")
    records = fetch_all_evaluations()
    if not records:
        st.info("No saved candidate evaluations found yet.")
    else:
        st.write(f"Total Evaluated Candidates: **{len(records)}**")
        table_data = []
        for r in records:
            table_data.append({
                "ID": r[0],
                "Candidate Name": r[1],
                "Email": r[2],
                "Job Role": r[3],
                "Match Score (%)": r[4],
                "Recommendation": r[5],
                "Date": r[6]
            })
        st.table(table_data)