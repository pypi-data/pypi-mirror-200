from collections import defaultdict
from copy import deepcopy

from idp_authentication.custom_types import UserRecordDict
from idp_authentication.enums import ChoiceEnum
from idp_authentication.users.base_classes.base_use_case import UseCasePort
from idp_authentication.users.domain.ports.unit_of_work import UsersUnitOfWorkPort

"""
{
   "username":"test",
   "first_name":"test",
   "last_name":"test",
   "email":"test@cardoai.com",
   "is_active":true,
   "is_staff":true,
   "is_superuser":true,
   "date_joined":"2022-01-01",
   "app_specific_configs":{
      "test":{
         "tenant":{
            "Servicer":{
               "app_entities_restrictions":{
                  "vehicle":[
                     1,
                     2
                  ]
               },
               "permission_restrictions":{
                  "synchronizeDoD":false
               }
            }
         }
      }
   }
}
"""


class ProcessUserMessageUseCase(UseCasePort):
    def __init__(
        self,
        users_unit_of_work: UsersUnitOfWorkPort,
        roles: ChoiceEnum,
        create_or_update_user_use_case: UseCasePort,
        tenants: list[str],
        app_identifier: str,
    ):
        self.users_unit_of_work = users_unit_of_work
        self.roles = roles

        self.data = None
        self.app_identifier = app_identifier
        self.create_or_update_user_user_case = create_or_update_user_use_case
        self.tenants = tenants or ["default"]

    def execute(self, data: UserRecordDict):
        """
        Extract tenants from the user record and call _update_user for each tenant.
        Remove tenant information from the payload of _update_user since it is not needed
        inside it.

        Send signals before and after calling the _update_user method for each tenant
        separately. This gives possibility to the project to react on the user update.

        One case of handling this signal is to switch database connection to the tenant's
        database. In this way the user can be updated in the correct database.

        """
        app_specific_configs = data.get("app_specific_configs", {})
        if self.app_identifier in app_specific_configs:
            self._process_user_data_with_access_to_app(data)
        else:
            self._verify_if_user_exists_and_delete_roles(username=data.get("username"))

    def _process_user_data_with_access_to_app(self, data: UserRecordDict):
        reported_user_app_configs = data.get("app_specific_configs", {}).get(
            self.app_identifier, {}
        )
        tenants = reported_user_app_configs.keys()
        for tenant in tenants:
            if tenant not in self.tenants:
                # logger.info(f"Tenant {tenant} not present, skipping.")
                continue

            user_record_for_tenant = deepcopy(data)
            user_record_for_tenant["app_specific_configs"] = reported_user_app_configs[
                tenant
            ]

            self._update_user(user_record_for_tenant)

    def _update_user(self, user_record: UserRecordDict):
        """
        This method makes sure that the changes that are coming from the IDP
        for a user are propagated in the internal product Authorization Schemas

        Step 1: Create or update User Object
        Step 2: Create/Update/Delete User Roles for this user.
        """
        user = self.create_or_update_user_user_case.execute(user_record)

        with self.users_unit_of_work as uow:
            # Get the user from the database again, to allow lazy loading of the user_roles
            # as the session that was used to create/delete the user is closed
            user = uow.user_repository.get_or_none(id=user.id)

            current_user_roles = defaultdict()
            for user_role in user.user_roles:
                current_user_roles[user_role.role] = user_role

            roles_data = user_record.get("app_specific_configs")
            for role, role_data in roles_data.items():
                if existing_user_role := current_user_roles.get(role):
                    uow.user_role_repository.update_record(
                        existing_user_role,
                        permission_restrictions=role_data.get(
                            "permission_restrictions"
                        ),
                        app_entities_restrictions=role_data.get(
                            "app_entities_restrictions"
                        ),
                    )
                else:
                    created_user_role = uow.user_role_repository.create(
                        user_id=user.id,
                        role=role,
                        permission_restrictions=role_data.get(
                            "permission_restrictions"
                        ),
                        app_entities_restrictions=role_data.get(
                            "app_entities_restrictions"
                        ),
                    )
                    user.user_roles.append(created_user_role)

            # Verify if any of the previous user roles is not being reported anymore
            # Delete it if this is the case
            for role, user_role in current_user_roles.items():
                if roles_data.get(role) is None:
                    # Delete Role Object
                    uow.user_role_repository.delete(user_role)
                    # Delete Role from User Object
                    uow.user_repository.remove_user_role(user, user_role)

            uow.commit()

    def _verify_if_user_exists_and_delete_roles(self, username: str):
        """
        Having arrived here means that the user does not have access in the current app
        Verify however if the user already exists in the database of any tenant
        If this is the case, delete his/her roles.
        """
        for tenant in self.tenants:
            with self.users_unit_of_work as uow:
                if user := uow.user_repository.get_or_none(username=username):
                    print(f"Deleting roles for user {username} in tenant {tenant}")

                    for user_role in user.user_roles:
                        uow.user_role_repository.delete(user_role)
                        uow.user_repository.remove_user_role(user, user_role)

                    uow.commit()
