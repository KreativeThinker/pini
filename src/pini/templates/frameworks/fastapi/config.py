import os
from dataclasses import dataclass
from enum import Enum
from typing import List

import dotenv

dotenv.load_dotenv()


class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


@dataclass
class Config:
    # Gunicorn
    gunicorn_workers: int = int(os.getenv("GUNICORN_WORKERS", 4))
    gunicorn_timeout: int = int(os.getenv("GUNICORN_TIMEOUT", 120))
    gunicorn_bind: str = os.getenv("GUNICORN_BIND", "0.0.0.0:8000")
    gunicorn_worker_class: str = os.getenv(
        "GUNICORN_WORKER_CLASS", "uvicorn.workers.UvicornWorker"
    )

    # App
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    environment: Environment = Environment(
        os.getenv("ENVIRONMENT", Environment.DEVELOPMENT.value)
    )

    # JWT
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "your-secret-key")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_expiration_minutes: int = int(os.getenv("JWT_EXPIRATION_MINUTES", 60))

    # Database
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")

    # CORS
    cors_origins: List[str] = os.getenv("CORS_ORIGINS", "*").split(",")

    # Logging
    log_level: LogLevel = LogLevel(os.getenv("LOG_LEVEL", LogLevel.INFO.value))

    # Email (optional)
    email_host: str = os.getenv("EMAIL_HOST", "")
    email_port: int = int(os.getenv("EMAIL_PORT", 587))
    email_username: str = os.getenv("EMAIL_USERNAME", "")
    email_password: str = os.getenv("EMAIL_PASSWORD", "")
    email_from: str = os.getenv("EMAIL_FROM", "")

    # Rate limiting (optional)
    rate_limit_requests: int = int(os.getenv("RATE_LIMIT_REQUESTS", 100))
    rate_limit_minutes: int = int(os.getenv("RATE_LIMIT_MINUTES", 1))


config: Config = Config()
