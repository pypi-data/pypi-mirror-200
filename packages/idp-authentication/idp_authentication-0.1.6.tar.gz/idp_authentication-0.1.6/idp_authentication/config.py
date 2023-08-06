from enum import Enum, unique
from os import getenv

from pydantic import BaseSettings, Field


def get_postgres_uri(dbname, user, password, host, port=5432):
    return f"postgresql://{user}:{password}@{host}:{port}/{dbname}"


def get_db_url() -> str:
    return get_postgres_uri(
        dbname=getenv("DATABASE_NAME"),
        user=getenv("DATABASE_USER"),
        password=getenv("DATABASE_PASSWORD"),
        host=getenv("DATABASE_HOST"),
    )


def get_test_memory_db_uri():
    return "sqlite:///:memory:"


@unique
class AppEnv(Enum):
    DEV = "development"
    STAGING = "staging"
    PROD = "production"


class Config(BaseSettings):
    APP_IDENTIFIER: str = Field(..., env="APP_IDENTIFIER")
    TENANTS: list = Field(..., env="TENANTS")
    ROLES: list = Field(..., env="ROLES")
    APP_ENTITY_TYPES: list = Field(..., env="APP_ENTITY_TYPES")
