from datetime import datetime

from idp_authentication.custom_types import AppEntityEventMessage
from idp_authentication.users.base_classes.base_use_case import UseCasePort
from idp_authentication.users.domain.entities.app_entity import AppEntity
from idp_authentication.users.domain.ports.event_producer import EventProducerPort


class SendAppEntityRecordEventUseCase(UseCasePort):
    def __init__(
        self,
        event_producer: EventProducerPort,
        app_identifier: str,
    ):
        self.event_producer = event_producer
        self.app_identifier = app_identifier

    def execute(self, app_entity_record: AppEntity, deleted: bool = False):
        app_entity_record_event: AppEntityEventMessage = {
            "app_identifier": self.app_identifier,
            "app_entity_type": app_entity_record.entity_type,
            "record_identifier": app_entity_record.idp_identifier,
            "label": app_entity_record.idp_label,
            "deleted": deleted,
        }
        self.event_producer.produce(
            topic="app_entity_record_events",
            key=str(datetime.now()),
            value=app_entity_record_event,
        )
