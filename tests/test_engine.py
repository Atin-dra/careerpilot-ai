from agents.engine import run_pipeline

def test_demo_pipeline():
    resume = "Python Java React SQL AWS Git REST API"
    jd = "Junior Engineer\nRequired: Python Java React SQL AWS Git REST API"
    report = run_pipeline(resume, jd, demo_mode=True)
    assert report.gap.fit_score == 100
    assert "python" in report.gap.matched
    assert len(report.interview_questions) > 0
