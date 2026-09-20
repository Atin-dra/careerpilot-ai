from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class JobAnalysis(BaseModel):
    title: str
    responsibilities: List[str] = Field(default_factory=list)
    required_skills: List[str] = Field(default_factory=list)
    nice_to_have: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)

class ResumeAnalysis(BaseModel):
    skills: List[str] = Field(default_factory=list)
    projects: List[str] = Field(default_factory=list)
    evidence: Dict[str, str] = Field(default_factory=dict)
    summary: str = ""

class GapAnalysis(BaseModel):
    matched: List[str] = Field(default_factory=list)
    gaps: List[str] = Field(default_factory=list)
    partial: List[str] = Field(default_factory=list)
    fit_score: int = 0
    explanation: str = ""

class ApplicationPlan(BaseModel):
    priorities: List[str] = Field(default_factory=list)
    seven_day_plan: List[str] = Field(default_factory=list)
    resume_changes: List[str] = Field(default_factory=list)

class FinalReport(BaseModel):
    job: JobAnalysis
    resume: ResumeAnalysis
    gap: GapAnalysis
    plan: ApplicationPlan
    recruiter_message: str
    interview_questions: List[str]
