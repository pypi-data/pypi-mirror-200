from idp_authentication.users.domain.ports.event_producer import EventProducerPort


class MockEventProducer(EventProducerPort):
    def __init__(self):
        self.topic = None
        self.key = None
        self.value = None

    def produce(self, topic: str, key: str, value: dict):
        self.topic = topic
        self.key = key
        self.value = value
