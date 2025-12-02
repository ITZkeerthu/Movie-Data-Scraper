from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    WIKIPEDIA_RATE_LIMIT: float = Field(1.0, env="WIKIPEDIA_RATE_LIMIT")  # requests per second
    RETRY_COUNT: int = Field(3, env="RETRY_COUNT")
    BATCH_SIZE: int = Field(100, env="BATCH_SIZE")
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
