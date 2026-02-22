from fastapi import APIRouter

from app.api.v1.endpoints.job_applications import router as applications_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(applications_router)
