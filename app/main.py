import json
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
import streamlit as st
from agents.engine import run_pipeline

st.set_page_config(page_title="CareerPilot AI", page_icon="🤖", layout="wide")

st.title("🤖 CareerPilot AI")
st.caption("Agentic Generative AI copilot for smarter, evidence-based job applications")

with st.sidebar:
    st.header("Configuration")
    demo = st.toggle("Demo Mode", value=True, help="Works without an API key using deterministic local agents.")
    st.markdown("**Agent pipeline**")
    for x in ["JD Analyst", "Resume Analyst", "Gap Analyst", "Application Strategist", "Communication Agent", "Interview Coach"]:
        st.write("✓ " + x)

col1, col2 = st.columns(2)
with col1:
    resume = st.text_area("📄 Paste your resume", height=420, placeholder="Paste resume text here...")
with col2:
    jd = st.text_area("💼 Paste the job description", height=420, placeholder="Paste job description here...")

c1, c2 = st.columns([1, 5])
with c1:
    analyze = st.button("🚀 Analyze", type="primary", use_container_width=True)
with c2:
    st.info("Tip: use the sample files in data/ for your first demo.")

if analyze:
    if not resume.strip() or not jd.strip():
        st.error("Please provide both a resume and a job description.")
    else:
        with st.spinner("Agents are analyzing the role, profile and application strategy..."):
            report = run_pipeline(resume, jd, demo_mode=demo)
        st.success("Analysis complete — the agents produced an application plan.")

        a, b, c = st.columns(3)
        a.metric("Role Fit", f"{report.gap.fit_score}%")
        b.metric("Matched Skills", len(report.gap.matched))
        c.metric("Skill Gaps", len(report.gap.gaps))

        tabs = st.tabs(["🎯 Fit Analysis", "🧭 Action Plan", "💬 Recruiter Message", "🎤 Interview Prep", "🧩 Agent State"])
        with tabs[0]:
            st.subheader(report.job.title)
            st.write(report.gap.explanation)
            left, right = st.columns(2)
            with left:
                st.markdown("### Matched")
                for x in report.gap.matched: st.success(x)
                st.markdown("### Partial")
                for x in report.gap.partial: st.warning(x)
            with right:
                st.markdown("### Gaps to strengthen")
                for x in report.gap.gaps: st.error(x)
            st.markdown("### Resume evidence")
            st.json(report.resume.evidence)
        with tabs[1]:
            st.markdown("### Priority areas")
            for x in report.plan.priorities: st.write("• " + x)
            st.markdown("### 7-day plan")
            for x in report.plan.seven_day_plan: st.write(x)
            st.markdown("### Resume changes")
            for x in report.plan.resume_changes: st.write("• " + x)
        with tabs[2]:
            st.text_area("Ready-to-edit message", report.recruiter_message, height=220)
        with tabs[3]:
            for i, q in enumerate(report.interview_questions, 1):
                st.write(f"**{i}.** {q}")
        with tabs[4]:
            st.json(report.model_dump())

        st.download_button(
            "⬇️ Download JSON report",
            data=json.dumps(report.model_dump(), indent=2),
            file_name="careerpilot_report.json",
            mime="application/json",
        )

st.divider()
st.caption("CareerPilot AI is an application assistant. It should not be used to make hiring decisions or infer protected characteristics.")
