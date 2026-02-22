from datetime import datetime
from typing import Optional

from pydantic import BaseModel, HttpUrl, ConfigDict

from app.models.job_application import ApplicationStatus


class JobApplicationCreate(BaseModel):
    company: str
    role: str
    job_url: Optional[str] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None
    status: ApplicationStatus = ApplicationStatus.PENDING
    resume_version: Optional[str] = None
    notes: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    applied_at: Optional[datetime] = None


class JobApplicationUpdate(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    job_url: Optional[str] = None
    location: Optional[str] = None
    salary_range: Optional[str] = None
    status: Optional[ApplicationStatus] = None
    resume_version: Optional[str] = None
    notes: Optional[str] = None
    follow_up_date: Optional[datetime] = None
    applied_at: Optional[datetime] = None


class JobApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company: str
    role: str
    job_url: Optional[str]
    location: Optional[str]
    salary_range: Optional[str]
    status: ApplicationStatus
    resume_version: Optional[str]
    notes: Optional[str]
    follow_up_date: Optional[datetime]
    applied_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime


class DashboardStats(BaseModel):
    total: int
    by_status: dict[str, int]
    follow_ups_due: int
    latest_applications: list[JobApplicationResponse]
