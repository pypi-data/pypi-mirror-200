from sqlalchemy import Boolean, Column, Date, DateTime, String

from idp_authentication.users.infrastructure.database.sqlalchemy.base import (
    Base,
    BaseModelMixin,
)


class UserModel(Base, BaseModelMixin):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_superuser = Column(Boolean, nullable=False, default=False)
    is_staff = Column(Boolean, nullable=False, default=False)
    last_login = Column(DateTime, nullable=True)
    date_joined = Column(Date, nullable=True)
