# CareerPilot AI — Agentic Job Application Copilot

CareerPilot AI is an agentic Generative AI application that helps job seekers turn a job description and resume into an actionable, personalized application strategy.

## Real-world problem

Job seekers repeatedly perform the same work for every application:
- understand a job description
- compare requirements with their resume
- find missing skills
- decide what to prioritize
- tailor their profile
- write recruiter outreach
- prepare for likely interview topics

CareerPilot AI automates this workflow through a small agent system instead of producing one generic chatbot response.

## What makes it agentic?

The system uses a coordinator that routes work through specialized agents:

1. **JD Analyst Agent** — extracts role, skills, responsibilities and keywords.
2. **Resume Analyst Agent** — extracts skills, projects, experience and evidence.
3. **Gap Analyst Agent** — compares requirements with candidate evidence and identifies gaps.
4. **Application Strategist Agent** — creates a prioritized 7-day preparation/application plan.
5. **Communication Agent** — generates a concise recruiter message grounded in the candidate's actual profile.
6. **Interview Coach Agent** — predicts role-relevant interview areas and creates practice questions.

The agents share structured state and the coordinator decides what should happen next.

## Features

- Resume + Job Description input
- Explainable fit analysis
- Required vs matched vs gap skills
- Evidence-based recommendations
- Tailored recruiter message
- 7-day action plan
- Interview preparation questions
- Demo mode with no API key required
- Optional OpenAI-powered generation
- Downloadable JSON report
- Streamlit web UI

## Architecture

```text
                 +-------------------+
                 |   Streamlit UI    |
                 +---------+---------+
                           |
                           v
                 +-------------------+
                 | Agent Coordinator  |
                 +---------+---------+
                           |
       +-------------------+--------------------+
       |          |           |        |        |
       v          v           v        v        v
   JD Agent  Resume Agent  Gap Agent  Strategy  Interview
                                      Agent      Agent
       |          |           |        |        |
       +----------+-----------+--------+--------+
                           |
                           v
                 +-------------------+
                 | Structured Report |
                 +-------------------+
```

## Tech stack

- Python
- Streamlit
- OpenAI API (optional)
- Pydantic
- python-dotenv
- Rule-based fallback/demo mode

## Run locally

### 1. Clone

```bash
git clone https://github.com/YOUR_USERNAME/careerpilot-ai.git
cd careerpilot-ai
```

### 2. Install

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Optional API key

Copy `.env.example` to `.env` and add an OpenAI API key.

Without an API key, the app still works in **Demo Mode** using deterministic local logic.

### 4. Start

```bash
streamlit run app/main.py
```

Open the URL shown by Streamlit, normally `http://localhost:8501`.

## Example demo

Use the included sample data:

- Resume: `data/sample_resume.txt`
- Job Description: `data/sample_job_description.txt`

The demo produces:

- role summary
- matched skills
- skill gaps
- evidence-backed recommendations
- recruiter message
- 7-day plan
- interview questions

## Resume bullets

**CareerPilot AI — Agentic Job Application Copilot**  
- Built an agentic Generative AI application using Python, Streamlit and structured multi-agent workflows to analyze resumes against job descriptions and generate personalized application strategies.
- Implemented specialized agents for job analysis, resume parsing, skill-gap detection, recruiter outreach and interview preparation with explainable, evidence-based outputs.
- Added an API-independent demo mode, structured Pydantic state, downloadable reports and a production-oriented architecture separating agents, tools and UI.

## Interview explanation

> “I built CareerPilot AI because applying to jobs manually is repetitive and difficult to personalize at scale. Instead of using one prompt, I split the workflow into specialized agents. The coordinator passes structured state from the job-analysis and resume-analysis agents to a gap-analysis agent, then the strategy and communication agents use those findings to create the final application plan. I also added a deterministic demo mode so the application works without an external LLM API.”

## Responsible-use note

The system is designed to assist applicants, not to make hiring decisions. It should not be used to infer protected characteristics or automatically reject candidates.
