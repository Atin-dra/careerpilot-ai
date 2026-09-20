import json
import os
import re
from typing import Any, Dict
from dotenv import load_dotenv
from openai import OpenAI
from .models import JobAnalysis, ResumeAnalysis, GapAnalysis, ApplicationPlan, FinalReport

load_dotenv()

SKILL_ALIASES = {
    "javascript": ["javascript", "js"],
    "react": ["react", "react.js", "reactjs"],
    "aws": ["aws", "amazon web services"],
    "rest api": ["rest api", "rest apis", "restful api"],
    "sql": ["sql"],
    "java": ["java"],
    "python": ["python"],
    "git": ["git", "github"],
    "node.js": ["node.js", "nodejs", "node"],
    "mongodb": ["mongodb", "mongo"],
    "docker": ["docker"],
    "ci/cd": ["ci/cd", "cicd", "continuous integration"],
    "networking": ["networking", "http"],
    "fastapi": ["fastapi"],
}

def _has(text: str, aliases):
    low = text.lower()
    return any(a in low for a in aliases)

def demo_job(jd: str) -> JobAnalysis:
    title = jd.splitlines()[0].strip() if jd.strip() else "Unknown Role"
    required = [k for k, a in SKILL_ALIASES.items() if _has(jd, a)]
    responsibilities = [x.strip("- ") for x in jd.splitlines() if x.strip().startswith("-")][:6]
    nice = []
    m = re.search(r"Nice to have:(.*)", jd, re.I | re.S)
    if m:
        nice = [k for k, a in SKILL_ALIASES.items() if _has(m.group(1), a)]
    return JobAnalysis(title=title, responsibilities=responsibilities, required_skills=required, nice_to_have=nice, keywords=required)

def demo_resume(resume: str) -> ResumeAnalysis:
    skills = [k for k, a in SKILL_ALIASES.items() if _has(resume, a)]
    projects = []
    for line in resume.splitlines():
        if "—" in line or "- Built" in line:
            projects.append(line.strip())
    return ResumeAnalysis(skills=skills, projects=projects[:5], evidence={k: f"Resume mentions {k}." for k in skills}, summary="Candidate has entry-level software, cloud and full-stack project exposure.")

def demo_gap(job: JobAnalysis, resume: ResumeAnalysis) -> GapAnalysis:
    matched, gaps, partial = [], [], []
    for skill in job.required_skills:
        if skill in resume.skills:
            matched.append(skill)
        elif skill == "networking" and "http" in resume.skills:
            partial.append(skill)
        else:
            gaps.append(skill)
    score = round((len(matched) + 0.5 * len(partial)) / max(1, len(job.required_skills)) * 100)
    return GapAnalysis(matched=matched, gaps=gaps, partial=partial, fit_score=score, explanation=f"Matched {len(matched)} of {len(job.required_skills)} detected required skills; {len(gaps)} need strengthening.")

def demo_plan(job, resume, gap):
    priorities = [f"Strengthen {x}" for x in gap.gaps[:4]] or ["Quantify project impact", "Practice role-specific interviews"]
    days = [
        "Day 1: Tailor resume summary and top project bullets to the job keywords.",
        "Day 2: Review AWS fundamentals and deployment concepts.",
        "Day 3: Practice REST API + SQL questions.",
        "Day 4: Build or review one React feature and explain the design.",
        "Day 5: Practice debugging and networking scenarios.",
        "Day 6: Complete a timed Java/Python coding set.",
        "Day 7: Mock interview and send a personalized recruiter message.",
    ]
    changes = [f"Mention concrete evidence for {x} where truthful." for x in gap.matched[:5]]
    return ApplicationPlan(priorities=priorities, seven_day_plan=days, resume_changes=changes)

def demo_message(job, resume, gap):
    matched = ", ".join(gap.matched[:5])
    return f"Hi, I’m a 2026 B.Tech graduate with hands-on project experience in {matched or 'software development'}, including APIs, frontend development and cloud fundamentals. I’m interested in the {job.title} opportunity and would be grateful if you could consider my profile for a suitable entry-level opening. I’d be happy to share my resume. Thank you."

def demo_questions(job, gap):
    topics = gap.matched[:5] + gap.gaps[:3]
    return [f"Explain how you would use {t} in a real project." for t in topics] + ["Walk me through a production bug you diagnosed and how you isolated the root cause.", "How would you design and secure a REST API?"]

def _llm_json(prompt: str) -> Dict[str, Any]:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not configured")
    client = OpenAI(api_key=key)
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    response = client.chat.completions.create(
        model=model,
        temperature=0.2,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are an evidence-grounded career analysis agent. Never invent candidate experience. Return valid JSON only."},
            {"role": "user", "content": prompt},
        ],
    )
    return json.loads(response.choices[0].message.content)

def run_pipeline(resume: str, jd: str, demo_mode: bool = True) -> FinalReport:
    if demo_mode or not os.getenv("OPENAI_API_KEY"):
        job = demo_job(jd)
        res = demo_resume(resume)
        gap = demo_gap(job, res)
        plan = demo_plan(job, res, gap)
        msg = demo_message(job, res, gap)
        questions = demo_questions(job, gap)
        return FinalReport(job=job, resume=res, gap=gap, plan=plan, recruiter_message=msg, interview_questions=questions)

    data = _llm_json(f"""
Analyze the job description and resume. Do not infer skills not supported by the resume.
JOB DESCRIPTION:\n{jd}\n\nRESUME:\n{resume}
Return JSON with keys: job, resume, gap, plan, recruiter_message, interview_questions.
job fields: title, responsibilities, required_skills, nice_to_have, keywords.
resume fields: skills, projects, evidence, summary.
gap fields: matched, gaps, partial, fit_score, explanation.
plan fields: priorities, seven_day_plan, resume_changes.
interview_questions: list of strings.
""")
    return FinalReport.model_validate(data)
