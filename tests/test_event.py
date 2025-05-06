from datetime import datetime
from app.mixins import CRUDMixin
from app.models.events import Event


def test_create_event(session, event_data):
    crud = CRUDMixin(session)
    event = crud.create(Event, **event_data)
    assert event is not None
    for key, value in event_data.items():
        assert getattr(event, key) == value


def test_update_event(session, event_data):
    crud = CRUDMixin(session)
    event = crud.create(Event, **event_data)
    updated_event = crud.update(Event, event.id, attendees=100)
    assert updated_event.attendees == 100


def test_delete_event(session, event_data):
    crud = CRUDMixin(session)
    event = crud.create(Event, **event_data)
    deleted_event = crud.delete(Event, event.id)
    assert deleted_event is not None
    deleted_event_check = session.query(Event).filter_by(id=event.id).first()
    assert deleted_event_check is None


def test_list_events(session, event_data):
    crud = CRUDMixin(session)
    crud.create(Event, **event_data)
    crud.create(
        Event,
        title="Conférence de gestion",
        contract_id=2,
        client_id=1,
        support_contact_id=1,
        start_datetime=datetime.now(),
        end_datetime=datetime.now(),
        location="Paris",
        attendees=40,
        notes="Notes",
    )
    events = crud.list(Event)
    assert len(events) >= 2
    assert any(e.title == "Conférence annuelle" for e in events)
    assert any(e.title == "Conférence de gestion" for e in events)
