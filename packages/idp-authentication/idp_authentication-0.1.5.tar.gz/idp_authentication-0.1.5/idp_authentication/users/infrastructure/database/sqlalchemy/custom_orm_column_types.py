import json

from sqlalchemy import String, TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as POSTGRES_UUID


class UUID(TypeDecorator):
    impl = String(36)
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(POSTGRES_UUID)
        else:
            return dialect.type_descriptor(self.impl)


class JsonField(TypeDecorator):
    impl = String()
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            return dialect.type_descriptor(JSONB)
        else:
            return dialect.type_descriptor(self.impl)

    def process_bind_param(self, value, dialect):
        if dialect.name == "postgresql":
            return value
        return json.dumps(value) if value else None

    def process_result_value(self, value, dialect):
        if dialect.name == "postgresql":
            return value
        return json.loads(value) if value else None
