from typing import Any

from idp_authentication.users.base_classes.base_repository import BaseRepository
from idp_authentication.users.domain.entities.user import User
from idp_authentication.users.domain.entities.user_role import UserRole
from idp_authentication.users.domain.ports.repository import UserRepositoryPort


class UserRepository(UserRepositoryPort, BaseRepository):
    entity = User

    def get_users_with_access_to_records(
        self,
        app_entity_type: str,
        record_identifier: Any,
        roles: list[str],
    ):
        """Get users with access to records."""

        user_roles_data = (
            self.session.query(UserRole.user_id, UserRole.app_entities_restrictions)
            .filter(UserRole.role.in_(roles))
            .all()
        )

        user_ids = []
        for user_id, app_entities_restrictions in user_roles_data:
            if app_entities_restrictions is None:
                user_ids.append(user_id)
            elif app_entity_type in app_entities_restrictions:
                app_entity_restriction = app_entities_restrictions[app_entity_type]
                if (
                    app_entity_restriction is None
                    or record_identifier in app_entity_restriction
                ):
                    user_ids.append(user_id)

        return (
            self.session.query(User)
            .filter(
                User.is_active.is_(True),
                User.id.in_(user_ids),
            )
            .all()
        )

    def remove_user_role(self, user: User, role: UserRole):
        user.user_roles.remove(role)
