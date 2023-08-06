<p align="center">
  <a href="https://cardoai.com/"><img src="https://cardoai.com/wp-content/themes/yootheme/cache/logo-cardo-negativo-cd27a0ee.webp" alt="FastAPI"></a>
</p>
<p align="center">
    <em>IDP Authentication hexagonal architecture implementation</em>
</p>

---

## Purpose

This project handles the authentication process of the Cardo platform. It is a hexagonal architecture implementation, which means that the business logic is independent of the framework used to implement the API.



## Architecture

The architecture is based on the [Hexagonal Architecture](https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)).

The main idea is to separate the business logic from the framework and the infrastructure.

The business logic is implemented in the `domain` module. This module is independent of the infrastructure.

The infrastructure is implemented `infrastructure` module.

The `app` which uses this package itself is the entry point of the application. It is the only module that depends on the framework.


## Project layout

    idp_authentication/
    ├── infrastructure
    │   ├── custom_orm_column_types.py
    │   ├── database.py
    │   ├── orm.py
    ├── users
    │   ├── adapters
    │   │   ├── orm.py
    │   │   ├── unit_of_work.py
    │   │   ├── events
    │   │   ├── repositories
    │   ├── base_classes
    │   │   ├── base_entity.py
    │   │   ├── base_repository.py
    │   ├── di
    │   │   ├── containers.py
    │   ├── domain
    │   │   ├── entities
    │   │   ├── ports
    │   │   ├── use_cases
    │   ├── infrastructure
    │   │   ├── database
    │   │   │   ├── sqlalchemy
    │   │   ├── faust
    │   │   │   ├── faust_app.py
    │   ├── tests
    │   │   ├── domain
    │   │   │   ├── __init__.py


## Requirements

Python 3.9+

IDP Authentication requires the following to be implemented:

* <a href="https://python-dependency-injector.ets-labs.org/" class="external-link" target="_blank">Dependency Injector</a>


## Installation
Since this is a private repository, you need to install the package with the following command:

    pip install git+ssh://git@github.com/CardoAI/idp-authentication.git@main


## Example

### Usage
Inside your application container:

```python3
from dependency_injector import providers
from idp_authentication.users.di.containers import UsersModuleDIContainer

    users_module = providers.Container(
        UsersModuleDIContainer,
        config=config,
        database=database,
    )
```


### Extending default config

```python3
from idp_authentication.config import Config

class TestConfig(Config):
    APP_IDENTIFIER = "test"
    TENANTS = ["default"]
    ROLES = [TEST_ROLE_1, TEST_ROLE_2]
    APP_ENTITY_TYPES = ["app_entity_1", "app_entity_2"]

    class Config:
        env_file_encoding = "utf-8"
        use_enum_values = True
```


### Configuration example

```python3
from dependency_injector import containers, providers
from idp_authentication.users.di.containers import UsersModuleDIContainer


class YourTestContainer(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[TestConfig()])
    url = get_test_memory_db_uri()
    database = providers.Singleton(
        Database,
    )
    users_module = providers.Container(
        UsersModuleDIContainer,
        config=config,
        database=database,
    )
```


### Usage example

```python3
    def container():
        container = YourTestContainer()
        container.wire(packages=["idp_authentication"]) # Wire IDPAuthentication
        container.users_module.start_mappers() # Start Users Module mapper
        yield container
```


### App Entity

To declare a new AppEntity, the Entity class should:
- Inherit from the class `AppEntity`
- Declare the properties `idp_identifier`, `idp_label` and optionally `entity_type`
- Example:
  ```python3
  from idp_authentication.users.domain.entities.app_entity import AppEntity
    
  class TestEntity(AppEntity):
        @property
        def idp_identifier(self):
            return self.id
          
        @property
        def idp_label(self):
            return self.name
    
        @property
        def entity_type(self):
            return "test"
  ```

