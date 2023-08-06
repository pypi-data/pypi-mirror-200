import uuid
from dataclasses import dataclass, field

import pytest as pytest
from dependency_injector import containers, providers
from faker import Faker
from sqlalchemy import Column, String, create_engine, orm
from sqlalchemy.orm import Session, mapper
from sqlalchemy.pool import NullPool

from idp_authentication.config import Config, get_test_memory_db_uri
from idp_authentication.users.base_classes.singleton import Singleton
from idp_authentication.users.di.containers import UsersModuleDIContainer
from idp_authentication.users.domain.entities import AppEntity, User, UserRole
from idp_authentication.users.infrastructure.database.sqlalchemy.base import (
    Base,
    BaseModelMixin,
)
from idp_authentication.users.infrastructure.database.sqlalchemy.custom_orm_column_types import (
    UUID,
)
from idp_authentication.users.tests.mock_event_producer import MockEventProducer

fake = Faker()

TEST_ROLE_1 = "TestRole_1"
TEST_ROLE_2 = "TestRole_2"
VEHICLE_APP_ENTITY_IDENTIFIER = "vehicle"
TEST_PERMISSION = "TestPermission"


class TestConfig(Config):
    APP_IDENTIFIER = "test"
    TENANTS = ["default"]
    ROLES = [TEST_ROLE_1, TEST_ROLE_2]
    APP_ENTITY_TYPES = [VEHICLE_APP_ENTITY_IDENTIFIER]

    class Config:
        env_file_encoding = "utf-8"
        use_enum_values = True


@dataclass(kw_only=True)
class Vehicle(AppEntity):
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    identifier: str = field(default_factory=str)
    label: str = field(default_factory=str)

    @property
    def idp_identifier(self):
        return self.identifier

    @property
    def idp_label(self):
        return self.label


class VehicleModel(Base, BaseModelMixin):
    __tablename__ = "vehicles"
    __table_args__ = {"extend_existing": True}

    id = Column(UUID(), primary_key=True, unique=True)
    identifier = Column(String(100), nullable=False, unique=True)
    label = Column(String(100), nullable=False)


def start_test_mappers():
    mapper(
        Vehicle,
        VehicleModel.__table__,
    )


class Database(metaclass=Singleton):
    def __init__(
        self, db_url: str, isolation_level: str = "REPEATABLE READ", pool_class=NullPool
    ) -> None:
        self.db_url = db_url
        self._engine = create_engine(db_url, isolation_level=isolation_level)
        self.session_factory = orm.scoped_session(
            orm.sessionmaker(
                expire_on_commit=False,
                autoflush=False,
                bind=self._engine,
                info={"debug": True},
            ),
        )

    def create_database(self) -> None:
        Base.metadata.create_all(self._engine)

    def drop_all(self) -> None:
        if "memory" in self.db_url:
            Base.metadata.drop_all(self._engine)


class TestContainer(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[TestConfig()])
    url = get_test_memory_db_uri()
    database = providers.Singleton(
        Database,
        db_url=url,
        isolation_level=config.ISOLATION_LEVEL,
    )
    event_producer = providers.Factory(MockEventProducer)
    users_module = providers.Container(
        UsersModuleDIContainer,
        config=config,
        database=database,
        event_producer=event_producer,
    )

    @staticmethod
    def __new__(cls, *args, **kwargs):
        container = super().__new__(cls, *args, **kwargs)
        container.users_module.start_mappers()
        return container


@pytest.fixture(scope="session")
def container():
    container = TestContainer()
    container.wire(packages=["idp_authentication"])
    start_test_mappers()
    database = container.database.provided()
    database.create_database()
    insert_initial_data(database.session_factory())

    yield container

    container.reset_override()
    database.drop_all()


@pytest.fixture(scope='function')
def session(container):
    s = container.database().session_factory()
    s.rollback()

    yield s

    s.rollback()
    s.close()


def insert_initial_data(session):
    user_1 = User(
        username="test1",
        email="test@test.com",
        first_name="test",
        last_name="test",
        is_active=True,
        is_superuser=False,
        is_staff=False,
        user_roles=[
            UserRole(
                role=TEST_ROLE_1,
                app_entities_restrictions={VEHICLE_APP_ENTITY_IDENTIFIER: [1, 2]},
                permission_restrictions={
                    TEST_PERMISSION: {VEHICLE_APP_ENTITY_IDENTIFIER: [1]}
                },
            )
        ],
    )
    user_2 = User(
        username="test2",
        email="test@test2.com",
        first_name="test2",
        last_name="test2",
        is_active=True,
        is_superuser=False,
        is_staff=False,
        user_roles=[
            UserRole(
                role=TEST_ROLE_2,
                app_entities_restrictions={VEHICLE_APP_ENTITY_IDENTIFIER: [3]},
                permission_restrictions={
                    TEST_PERMISSION: {VEHICLE_APP_ENTITY_IDENTIFIER: [4]}
                },
            )
        ],
    )
    user_3 = User(
        username="test3",
        email="test@test3.com",
        first_name="test3",
        last_name="test3",
        is_active=True,
        is_superuser=False,
        is_staff=False,
    )
    vehicle = Vehicle(identifier="1", label="vehicle1")
    vehicle_2 = Vehicle(identifier="2", label="vehicle2")
    objects = [user_1, user_2, user_3, vehicle, vehicle_2]
    session.add_all(objects)
    session.commit()


@pytest.fixture(scope="function")
def user(container, session):
    return session.query(User).filter(User.username == "test1").first()


@pytest.fixture(scope="function")
def user_2(container, session):
    return session.query(User).filter(User.username == "test2").first()


@pytest.fixture(scope="function")
def user_without_role(container, session):
    return session.query(User).filter(User.username == "test3").first()


@pytest.fixture(scope="function")
def make_user(container, session):
    def create_user(**overrides):
        default_data = {
            "username": fake.user_name(),
            "email": fake.email(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "is_active": True,
            "is_superuser": False,
            "is_staff": False,
            "user_roles": [
                UserRole(
                    role=TEST_ROLE_1,
                    app_entities_restrictions={VEHICLE_APP_ENTITY_IDENTIFIER: [1, 2]},
                    permission_restrictions={
                        TEST_PERMISSION: {VEHICLE_APP_ENTITY_IDENTIFIER: [1]}
                    },
                )
            ],
        }
        default_data.update(overrides)

        user = User(**default_data)

        session.add(user)
        session.commit()

        return user

    return create_user


@pytest.fixture(scope="function")
def vehicle(container, session):
    return session.query(Vehicle).first()
