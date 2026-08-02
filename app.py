import streamlit as st

from services.pdf_loadder import extract_text_from_pdf
from graph.workflow import recruitment_graph

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="AI HR Recruitment Assistant",
    page_icon="💼",
    layout="wide"
)

st.title("💼 AI HR Recruitment Assistant")
st.markdown(
    "Upload a candidate resume and paste a job description."
)

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.header("Project Info")

st.sidebar.success("Sequential Workflow")

st.sidebar.write("""
1. Resume Extraction
2. Resume Screening
3. Skill Matching
4. Interview Questions
5. Candidate Summary
""")

# -----------------------------
# Inputs
# -----------------------------
uploaded_pdf = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=250
)

# -----------------------------
# Read PDF
# -----------------------------
resume_text = ""

if uploaded_pdf is not None:

    try:
        resume_text = extract_text_from_pdf(uploaded_pdf)
    except Exception as e:
        st.error(f"Could not read the PDF file: {e}")

# -----------------------------
# Display Resume
# -----------------------------
if resume_text:

    st.subheader("Extracted Resume Text")

    st.text_area(
        "Resume",
        resume_text,
        height=300
    )

# -----------------------------
# Display Job Description
# -----------------------------
if job_description:

    st.subheader("Job Description")

    st.text_area(
        "JD",
        job_description,
        height=250
    )

# -----------------------------
# Start Button
# -----------------------------
if st.button("Start Recruitment Workflow"):

    if uploaded_pdf is None:

        st.error("Please upload a resume.")

    elif not resume_text.strip():

        st.error(
            "No text could be extracted from this PDF. "
            "Please upload a text-based resume (not a scanned image)."
        )

    elif job_description.strip() == "":

        st.error("Please paste the job description.")

    else:

        # Initial state must match the RecruitmentState schema
        # defined in graph/state.py
        initial_state = {
            "resume_text": resume_text,
            "job_description": job_description,

            "candidate_name": None,
            "candidate_email": None,
            "candidate_phone": None,

            "education": "",
            "experience": "",

            "extracted_skills": [],

            "screening_result": "",

            "matched_skills": [],
            "missing_skills": [],
            "match_score": 0,

            "easy_questions": [],
            "intermediate_questions": [],
            "advanced_questions": [],

            "strengths": [],
            "weaknesses": [],
            "recommendation": "",
            "final_summary": "",

            "errors": [],
        }

        with st.spinner("Running the recruitment agents..."):
            try:
                result = recruitment_graph.invoke(initial_state)
            except Exception as e:
                st.error(f"The recruitment workflow failed: {e}")
                result = None

        if result is not None:

            st.success("✅ Workflow Complete")

            # -----------------------------
            # 1. Candidate Info
            # -----------------------------
            st.header("1️⃣ Candidate Information")

            col1, col2, col3 = st.columns(3)
            col1.metric("Name", result.get("candidate_name") or "N/A")
            col2.metric("Email", result.get("candidate_email") or "N/A")
            col3.metric("Phone", result.get("candidate_phone") or "N/A")

            st.write("**Education:**", result.get("education") or "N/A")
            st.write("**Experience:**", result.get("experience") or "N/A")
            st.write("**Extracted Skills:**",
                      ", ".join(result.get("extracted_skills") or []) or "N/A")

            # -----------------------------
            # 2. Screening
            # -----------------------------
            st.header("2️⃣ Resume Screening")
            st.write(result.get("screening_result") or "N/A")

            # -----------------------------
            # 3. Skill Matching
            # -----------------------------
            st.header("3️⃣ Skill Matching")

            st.metric("Match Score", f"{result.get('match_score', 0)}%")

            m_col1, m_col2 = st.columns(2)
            with m_col1:
                st.write("**✅ Matched Skills**")
                for skill in result.get("matched_skills") or []:
                    st.write(f"- {skill}")

            with m_col2:
                st.write("**❌ Missing Skills**")
                for skill in result.get("missing_skills") or []:
                    st.write(f"- {skill}")

            # -----------------------------
            # 4. Interview Questions
            # -----------------------------
            st.header("4️⃣ Interview Questions")

            with st.expander("Easy Questions"):
                for q in result.get("easy_questions") or []:
                    st.write(f"- {q}")

            with st.expander("Intermediate Questions"):
                for q in result.get("intermediate_questions") or []:
                    st.write(f"- {q}")

            with st.expander("Advanced Questions"):
                for q in result.get("advanced_questions") or []:
                    st.write(f"- {q}")

            # -----------------------------
            # 5. Candidate Summary
            # -----------------------------
            st.header("5️⃣ Candidate Summary")

            s_col1, s_col2 = st.columns(2)
            with s_col1:
                st.write("**Strengths**")
                for s in result.get("strengths") or []:
                    st.write(f"- {s}")

            with s_col2:
                st.write("**Weaknesses**")
                for w in result.get("weaknesses") or []:
                    st.write(f"- {w}")

            recommendation = result.get("recommendation") or "N/A"

            rec_colors = {
                "Hire": "success",
                "Technical Interview": "info",
                "Hold": "warning",
                "Reject": "error",
            }
            display_fn = getattr(st, rec_colors.get(recommendation, "info"))
            display_fn(f"**Recommendation:** {recommendation}")

            st.write("**Final Summary**")
            st.write(result.get("final_summary") or "N/A")

            if result.get("errors"):
                st.warning("Some steps reported issues:")
                for err in result["errors"]:
                    st.write(f"- {err}")
