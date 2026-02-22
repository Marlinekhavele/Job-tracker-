import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_create_application(client: AsyncClient):
    response = await client.post("/api/v1/applications/", json={
        "company": "N26",
        "role": "Senior Backend Engineer",
        "location": "Berlin, Germany",
        "salary_range": "€90k-€110k",
        "status": "applied",
        "resume_version": "v3",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["company"] == "N26"
    assert data["role"] == "Senior Backend Engineer"
    assert data["status"] == "applied"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_applications(client: AsyncClient):
    # Seed two applications
    await client.post("/api/v1/applications/", json={"company": "Zalando", "role": "Python Developer"})
    await client.post("/api/v1/applications/", json={"company": "Delivery Hero", "role": "Platform Engineer"})

    response = await client.get("/api/v1/applications/")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_filter_by_status(client: AsyncClient):
    await client.post("/api/v1/applications/", json={"company": "HelloFresh", "role": "Backend Dev", "status": "interview"})
    await client.post("/api/v1/applications/", json={"company": "Taxfix", "role": "Engineer", "status": "pending"})

    response = await client.get("/api/v1/applications/?status=interview")
    assert response.status_code == 200
    results = response.json()
    assert all(r["status"] == "interview" for r in results)


@pytest.mark.asyncio
async def test_get_application_not_found(client: AsyncClient):
    response = await client.get("/api/v1/applications/9999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_application_status(client: AsyncClient):
    create = await client.post("/api/v1/applications/", json={"company": "SumUp", "role": "Backend Engineer"})
    app_id = create.json()["id"]

    response = await client.patch(f"/api/v1/applications/{app_id}", json={"status": "offer"})
    assert response.status_code == 200
    assert response.json()["status"] == "offer"


@pytest.mark.asyncio
async def test_delete_application(client: AsyncClient):
    create = await client.post("/api/v1/applications/", json={"company": "Babbel", "role": "Senior Dev"})
    app_id = create.json()["id"]

    delete_response = await client.delete(f"/api/v1/applications/{app_id}")
    assert delete_response.status_code == 204

    get_response = await client.get(f"/api/v1/applications/{app_id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_dashboard_stats(client: AsyncClient):
    await client.post("/api/v1/applications/", json={"company": "Contentful", "role": "Dev", "status": "applied"})
    await client.post("/api/v1/applications/", json={"company": "Klarna", "role": "Dev", "status": "rejected"})

    response = await client.get("/api/v1/applications/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert "by_status" in data
    assert "follow_ups_due" in data
    assert "latest_applications" in data
