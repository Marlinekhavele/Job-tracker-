import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi import HTTPException

from app.models.job_application import ApplicationStatus
from app.schemas.job_application import JobApplicationCreate, JobApplicationUpdate
from app.services.job_application_service import JobApplicationService
from datetime import datetime


def _mock_application(overrides: dict = {}) -> MagicMock:
    app = MagicMock()
    app.id = 1
    app.company = "Stripe"
    app.role = "Backend Engineer"
    app.job_url = "https://stripe.com/jobs/123"
    app.location = "Berlin, Germany"
    app.salary_range = "€80k-€100k"
    app.status = ApplicationStatus.APPLIED
    app.resume_version = "v2"
    app.notes = "Applied via LinkedIn"
    app.follow_up_date = None
    app.applied_at = datetime(2024, 6, 1)
    app.created_at = datetime(2024, 6, 1)
    app.updated_at = datetime(2024, 6, 1)
    for k, v in overrides.items():
        setattr(app, k, v)
    return app


@pytest.mark.asyncio
async def test_create_application_returns_response():
    repo = MagicMock()
    repo.create = AsyncMock(return_value=_mock_application())
    service = JobApplicationService(repo)

    payload = JobApplicationCreate(company="Stripe", role="Backend Engineer")
    result = await service.create_application(payload)

    assert result.company == "Stripe"
    assert result.role == "Backend Engineer"
    repo.create.assert_called_once_with(payload)


@pytest.mark.asyncio
async def test_get_application_not_found_raises_404():
    repo = MagicMock()
    repo.get_by_id = AsyncMock(return_value=None)
    service = JobApplicationService(repo)

    with pytest.raises(HTTPException) as exc_info:
        await service.get_application(999)

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_update_application_not_found_raises_404():
    repo = MagicMock()
    repo.update = AsyncMock(return_value=None)
    service = JobApplicationService(repo)

    with pytest.raises(HTTPException) as exc_info:
        await service.update_application(999, JobApplicationUpdate(status=ApplicationStatus.INTERVIEW))

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_delete_application_not_found_raises_404():
    repo = MagicMock()
    repo.delete = AsyncMock(return_value=False)
    service = JobApplicationService(repo)

    with pytest.raises(HTTPException) as exc_info:
        await service.delete_application(999)

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_get_dashboard_stats():
    repo = MagicMock()
    repo.count_by_status = AsyncMock(return_value={ApplicationStatus.APPLIED: 3, ApplicationStatus.REJECTED: 1})
    repo.get_follow_ups_due = AsyncMock(return_value=2)
    repo.get_recent = AsyncMock(return_value=[_mock_application()])

    service = JobApplicationService(repo)
    stats = await service.get_dashboard_stats()

    assert stats.total == 4
    assert stats.follow_ups_due == 2
    assert len(stats.latest_applications) == 1
