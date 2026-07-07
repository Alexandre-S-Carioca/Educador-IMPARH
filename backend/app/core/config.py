from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Educador API"
    SECRET_KEY: str = "super_secret_key_change_in_production"  # Mudar em produção
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 dias
    DATABASE_URL: str = "postgresql+psycopg2://educador_user:educador_password@localhost:5433/educador_dev"
    GEMINI_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None
    AI_PROVIDER: str = "groq"
    GROQ_MODEL: str = "llama-3.1-8b-instant"


    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

settings = Settings()
