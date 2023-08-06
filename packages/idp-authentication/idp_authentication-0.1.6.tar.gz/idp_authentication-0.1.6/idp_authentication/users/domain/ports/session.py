from abc import ABC

from sqlalchemy.orm import Session


class SessionPort(Session, ABC):
    pass
