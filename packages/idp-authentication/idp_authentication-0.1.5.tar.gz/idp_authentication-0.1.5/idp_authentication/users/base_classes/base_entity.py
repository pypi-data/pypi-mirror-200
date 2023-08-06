import uuid
from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class BaseEntity(ABC):
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
