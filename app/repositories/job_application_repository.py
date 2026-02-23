from datetime import datetime, timezone
from typing import Sequence

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.job_application import JobApplication, ApplicationStatus
from app.schemas.job_application import JobApplicationCreate, JobApplicationUpdate


class JobApplicationRepository:
    """
    args:
        db: AsyncSession - The asynchronous database session for performing CRUD operations on job applications
    methods:
        create(payload: JobApplicationCreate) -> JobApplication - Creates a new job application record in the database
        get_by_id(application_id: int) -> JobApplication | None - Retrieves a job application by its ID, or returns None if not found
        get_all(status: ApplicationStatus | None, company: str | None, limit: int, offset: int) -> Sequence[JobApplication] - Retrieves a list of job applications with optional filtering by status and company, and supports pagination
        update(application_id: int, payload: JobApplicationUpdate) -> JobApplication | None - Updates an existing job application with the provided fields, or returns None if the application ID does not exist
        delete(application_id: int) -> bool - Deletes a job application by its ID, returning True if deletion was successful or False if the application ID does not exist
        count_by_status() -> dict[str, int] - Returns a dictionary with the count of job applications grouped by their status
        get_follow_ups_due() -> int - Returns the count of job applications that have a follow-up date that is due (i.e., in the past) and are not in a final status (rejected, withdrawn, offer)
        get_recent(limit: int) -> Sequence[JobApplication] - Retrieves the most recent job applications, limited by the specified number
    """
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create(self, payload: JobApplicationCreate) -> JobApplication:
        application = JobApplication(**payload.model_dump())
        self._db.add(application)
        await self._db.commit()
        await self._db.refresh(application)
        return application

    async def get_by_id(self, application_id: int) -> JobApplication | None:
        result = await self._db.execute(
            select(JobApplication).where(JobApplication.id == application_id)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        status: ApplicationStatus | None = None,
        company: str | None = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Sequence[JobApplication]:
        query = select(JobApplication)

        if status:
            query = query.where(JobApplication.status == status)
        if company:
            query = query.where(JobApplication.company.ilike(f"%{company}%"))

        query = query.order_by(JobApplication.created_at.desc()).limit(limit).offset(offset)
        result = await self._db.execute(query)
        return result.scalars().all()

    async def update(
        self, application_id: int, payload: JobApplicationUpdate
    ) -> JobApplication | None:
        application = await self.get_by_id(application_id)
        if not application:
            return None

        for field, value in payload.model_dump(exclude_unset=True).items():
            setattr(application, field, value)

        await self._db.commit()
        await self._db.refresh(application)
        return application

    async def delete(self, application_id: int) -> bool:
        application = await self.get_by_id(application_id)
        if not application:
            return False

        await self._db.delete(application)
        await self._db.commit()
        return True

    async def count_by_status(self) -> dict[str, int]:
        result = await self._db.execute(
            select(JobApplication.status, func.count(JobApplication.id))
            .group_by(JobApplication.status)
        )
        return {status.value: count for status, count in result.all()}

    async def get_follow_ups_due(self) -> int:
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        result = await self._db.execute(
            select(func.count(JobApplication.id)).where(
                JobApplication.follow_up_date <= now,
                JobApplication.status.notin_(
                    [ApplicationStatus.REJECTED, ApplicationStatus.WITHDRAWN, ApplicationStatus.OFFER]
                ),
            )
        )
        return result.scalar_one()

    async def get_recent(self, limit: int = 5) -> Sequence[JobApplication]:
        result = await self._db.execute(
            select(JobApplication)
            .order_by(JobApplication.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()
