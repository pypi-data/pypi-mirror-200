from sqlalchemy import Column, ForeignKey, String

from idp_authentication.users.infrastructure.database.sqlalchemy.base import (
    Base,
    BaseModelMixin,
)
from idp_authentication.users.infrastructure.database.sqlalchemy.custom_orm_column_types import (
    UUID,
    JsonField,
)


class UserRoleModel(Base, BaseModelMixin):
    __tablename__ = "user_roles"
    __table_args__ = {"extend_existing": True}

    user_id = Column(UUID(), ForeignKey("users.id"))
    role = Column(String(40), nullable=False)
    app_entities_restrictions = Column(JsonField(), nullable=True)
    permission_restrictions = Column(JsonField(), default=dict)
