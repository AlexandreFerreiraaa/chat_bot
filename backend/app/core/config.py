"""Configurações lidas do .env (nunca versionado)."""
import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-inseguro-troque-no-env")
    TOKEN_EXPIRA_MINUTOS: int = int(os.getenv("TOKEN_EXPIRA_MINUTOS", "120"))
    DATABASE_PATH: str = os.getenv("DATABASE_PATH", "chat.db")
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "simulado").lower()
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    LLM_TIMEOUT_SEGUNDOS: int = int(os.getenv("LLM_TIMEOUT_SEGUNDOS", "30"))


settings = Settings()
