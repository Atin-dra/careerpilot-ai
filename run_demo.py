from pathlib import Path
from agents.engine import run_pipeline

root = Path(__file__).parent
resume = (root / "data/sample_resume.txt").read_text()
jd = (root / "data/sample_job_description.txt").read_text()
report = run_pipeline(resume, jd, demo_mode=True)
print("Role:", report.job.title)
print("Fit:", report.gap.fit_score, "%")
print("Matched:", ", ".join(report.gap.matched))
print("Gaps:", ", ".join(report.gap.gaps))
print("\nRecruiter message:\n", report.recruiter_message)
