from fastapi import HTTPException, status

from app.models.job_application import ApplicationStatus, JobApplication
from app.repositories.job_application_repository import JobApplicationRepository
from app.schemas.job_application import (
    DashboardStats,
    JobApplicationCreate,
    JobApplicationResponse,
    JobApplicationUpdate,
)


class JobApplicationService:
    def __init__(self, repository: JobApplicationRepository) -> None:
        self._repo = repository

    async def create_application(
        self, payload: JobApplicationCreate
    ) -> JobApplicationResponse:
        application = await self._repo.create(payload)
        return JobApplicationResponse.model_validate(application)

    async def get_application(self, application_id: int) -> JobApplicationResponse:
        application = await self._repo.get_by_id(application_id)
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Application with id={application_id} not found.",
            )
        return JobApplicationResponse.model_validate(application)

    async def list_applications(
        self,
        status: ApplicationStatus | None = None,
        company: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> list[JobApplicationResponse]:
        applications = await self._repo.get_all(
            status=status, company=company, limit=limit, offset=offset
        )
        return [JobApplicationResponse.model_validate(a) for a in applications]

    async def update_application(
        self, application_id: int, payload: JobApplicationUpdate
    ) -> JobApplicationResponse:
        application = await self._repo.update(application_id, payload)
        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Application with id={application_id} not found.",
            )
        return JobApplicationResponse.model_validate(application)

    async def delete_application(self, application_id: int) -> None:
        deleted = await self._repo.delete(application_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Application with id={application_id} not found.",
            )

    async def get_dashboard_stats(self) -> DashboardStats:
        total_by_status = await self._repo.count_by_status()
        follow_ups_due = await self._repo.get_follow_ups_due()
        recent = await self._repo.get_recent(limit=5)

        total = sum(total_by_status.values())

        # Ensure all statuses are represented
        all_statuses = {s.value: 0 for s in ApplicationStatus}
        all_statuses.update(total_by_status)

        return DashboardStats(
            total=total,
            by_status=all_statuses,
            follow_ups_due=follow_ups_due,
            latest_applications=[JobApplicationResponse.model_validate(a) for a in recent],
        )
