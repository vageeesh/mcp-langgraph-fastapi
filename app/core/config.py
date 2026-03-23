from pathlib import Path
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    OPENAI_API_KEY: str
    OPENAI_MODEL: str
    MAX_HISTORY: int
    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        env_file = BASE_DIR / ".env"


settings = Settings()