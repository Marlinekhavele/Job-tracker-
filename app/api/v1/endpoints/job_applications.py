from fastapi import APIRouter, Depends, Query, status

from app.core.dependencies import get_job_application_service
from app.models.job_application import ApplicationStatus
from app.schemas.job_application import (
    DashboardStats,
    JobApplicationCreate,
    JobApplicationResponse,
    JobApplicationUpdate,
)
from app.services.job_application_service import JobApplicationService

router = APIRouter(prefix="/applications", tags=["Job Applications"])


@router.post(
    "/",
    response_model=JobApplicationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Track a new job application",
)
async def create_application(
    payload: JobApplicationCreate,
    service: JobApplicationService = Depends(get_job_application_service),
) -> JobApplicationResponse:
    return await service.create_application(payload)


@router.get(
    "/",
    response_model=list[JobApplicationResponse],
    summary="List all job applications with optional filters",
)
async def list_applications(
    status: ApplicationStatus | None = Query(default=None, description="Filter by status"),
    company: str | None = Query(default=None, description="Filter by company name"),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    service: JobApplicationService = Depends(get_job_application_service),
) -> list[JobApplicationResponse]:
    return await service.list_applications(
        status=status, company=company, limit=limit, offset=offset
    )


@router.get(
    "/dashboard",
    response_model=DashboardStats,
    summary="Get aggregated stats across all applications",
)
async def get_dashboard(
    service: JobApplicationService = Depends(get_job_application_service),
) -> DashboardStats:
    return await service.get_dashboard_stats()


@router.get(
    "/{application_id}",
    response_model=JobApplicationResponse,
    summary="Get a single application by ID",
)
async def get_application(
    application_id: int,
    service: JobApplicationService = Depends(get_job_application_service),
) -> JobApplicationResponse:
    return await service.get_application(application_id)


@router.patch(
    "/{application_id}",
    response_model=JobApplicationResponse,
    summary="Update application fields or status",
)
async def update_application(
    application_id: int,
    payload: JobApplicationUpdate,
    service: JobApplicationService = Depends(get_job_application_service),
) -> JobApplicationResponse:
    return await service.update_application(application_id, payload)


@router.delete(
    "/{application_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an application",
)
async def delete_application(
    application_id: int,
    service: JobApplicationService = Depends(get_job_application_service),
) -> None:
    await service.delete_application(application_id)
