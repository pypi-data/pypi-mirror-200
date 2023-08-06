import pytest

from idp_authentication.users.tests.mock_event_producer import MockEventProducer


@pytest.mark.parametrize(
    "deleted",
    [
        True,
        False,
    ],
)
def test_create_or_delete_app_entity_record_event(container, vehicle, deleted):
    # Arrange
    event_producer = MockEventProducer()

    # Act
    with container.event_producer.override(event_producer):
        use_case = (
            container.users_module.use_cases.send_app_entity_record_event_use_case.provided()
        )
        use_case.execute(app_entity_record=vehicle, deleted=deleted)

    # Assert
    assert event_producer.value == {
        "app_identifier": container.config.provided().get("APP_IDENTIFIER"),
        "app_entity_type": vehicle.entity_type,
        "record_identifier": vehicle.idp_identifier,
        "label": vehicle.idp_label,
        "deleted": deleted,
    }
