from typing import Any

from idp_authentication.users.domain.ports.unit_of_work import UnitOfWorkPort


class BaseUnitOfWork(UnitOfWorkPort):
    def __init__(self, session_maker: Any):
        self.session_maker = session_maker

    def __enter__(self):
        self.session = self.session_maker()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Implicit commit in case everything goes right.
        # Otherwise, the rollback gets executed.
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

        self.session_maker.remove()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
