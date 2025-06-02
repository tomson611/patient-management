"""Configuration settings for the application."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for application configuration."""

    SECRET_KEY: str
    ALGORITHM: str
    DATABASE_URL: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        """Pydantic configuration for environment file."""

        env_file = ".env"


settings = Settings()
