from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.job_application_repository import JobApplicationRepository
from app.services.job_application_service import JobApplicationService


def get_job_application_repository(db: AsyncSession = Depends(get_db)) -> JobApplicationRepository:
    return JobApplicationRepository(db)


def get_job_application_service(
    repository: JobApplicationRepository = Depends(get_job_application_repository),
) -> JobApplicationService:
    return JobApplicationService(repository)
