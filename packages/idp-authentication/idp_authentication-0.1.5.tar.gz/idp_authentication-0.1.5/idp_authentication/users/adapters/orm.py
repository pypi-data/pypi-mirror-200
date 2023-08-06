from sqlalchemy.event import listen
from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import mapper as orm_mapper
from sqlalchemy.orm import relationship

from idp_authentication.users.base_classes.base_use_case import UseCasePort
from idp_authentication.users.domain.entities import AppEntity, User, UserRole
from idp_authentication.users.infrastructure.database.sqlalchemy.user import UserModel
from idp_authentication.users.infrastructure.database.sqlalchemy.user_role import (
    UserRoleModel,
)


class AppEntitySignal:
    """
    AppEntitySignal is a class that listens to the events of the AppEntity class
    and calls the use case to execute the business logic.

    The use case is injected into the class via the constructor.

    Parameters
    ----------
    use_case : UseCasePort
        The use case to be called when the event is triggered.

    Methods
    -------
    receive_after_insert_or_update(mapper, connection, target)
        The method that is called when the AppEntity class is inserted or updated.

    receive_after_delete(mapper, connection, target)
        The method that is called when the AppEntity class is deleted.

    """

    def __init__(self, use_case):
        self.use_case: UseCasePort = use_case

    def receive_after_insert_or_update(
        self,
        mapper,
        connection,
        target: AppEntity,
    ):
        print("received insert/update event for", target.entity_type)
        self.use_case.execute(target)

    def receive_after_delete(
        self,
        mapper,
        connection,
        target: AppEntity,
    ):
        print("received delete event for", target.entity_type)
        self.use_case.execute(app_entity_record=target, deleted=True)


def start_mappers(send_event_use_case):
    """
    Starts mappers for User and UserRole entities between SQLAlchemy models and domain entities.

    Parameters
    ----------
    send_event_use_case : UseCasePort
        Use case to send events(signals)

    Returns
    -------
    None
    """
    try:
        print("Starting Users module mappers...")

        user_mapper = orm_mapper(
            User,
            UserModel.__table__,
            properties={
                "user_roles": relationship(
                    UserRole, back_populates="user", lazy="select"
                ),
            },
        )
        orm_mapper(
            UserRole,
            UserRoleModel.__table__,
            properties={
                "user": relationship(
                    user_mapper, back_populates="user_roles", uselist=False
                ),
            },
        )
        app_entity_signal = AppEntitySignal(send_event_use_case)
        listen(
            AppEntity,
            "after_insert",
            app_entity_signal.receive_after_insert_or_update,
            propagate=True,
        )
        listen(
            AppEntity,
            "after_update",
            app_entity_signal.receive_after_insert_or_update,
            propagate=True,
        )
        listen(
            AppEntity,
            "after_delete",
            app_entity_signal.receive_after_delete,
            propagate=True,
        )
    except ArgumentError as e:
        # Skip if mappers already started
        if "already has a primary mapper defined" not in str(e):
            raise e
