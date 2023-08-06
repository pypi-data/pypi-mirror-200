from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

from idp_authentication.users.base_classes.base_entity import BaseEntity
from idp_authentication.users.domain.entities.user_role import UserRole


@dataclass(kw_only=True)
class User(BaseEntity):
    username: str = field(default_factory=str)
    email: str = field(default_factory=str)
    first_name: str = field(default_factory=str)
    last_name: str = field(default_factory=str)
    is_active: bool = field(default_factory=bool)
    is_superuser: bool = field(default_factory=bool)
    is_staff: bool = field(default_factory=bool)
    last_login: Optional[datetime] = field(default=None)
    date_joined: Optional[date] = field(default=None)
    user_roles: Optional[list[UserRole]] = field(default_factory=list)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.first_name
