from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Job Application Tracker"
    app_version: str = "1.0.0"
    app_env: str = "development"
    database_url: str = "sqlite+aiosqlite:///./job_tracker.db"
    secret_key: str = "change-me-in-production"

    class Config:
        env_file = ".env"


settings = Settings()
