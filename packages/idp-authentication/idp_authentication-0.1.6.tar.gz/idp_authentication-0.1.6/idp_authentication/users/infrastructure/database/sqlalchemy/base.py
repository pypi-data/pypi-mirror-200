from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import declarative_base, declarative_mixin

from idp_authentication.users.infrastructure.database.sqlalchemy.custom_orm_column_types import (
    UUID,
)

Base = declarative_base()


@declarative_mixin
class BaseModelMixin:
    id = Column(
        UUID(), primary_key=True, unique=True
    )  # UUID will be used, which has 36 chars.
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
