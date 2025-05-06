from app.mixins import CRUDMixin
from app.models.client import Client


def test_create_client(session, client_data):
    # Créer une instance de CRUDMixin
    crud = CRUDMixin(session)
    client = crud.create(Client, **client_data)
    assert client is not None
    for key, value in client_data.items():
        assert getattr(client, key) == value


def test_update_client(session, client_data):
    crud = CRUDMixin(session)
    client = crud.create(Client, **client_data)
    updated_client = crud.update(Client, client.id, name="Updated Client Name")
    assert updated_client.name == "Updated Client Name"


def test_delete_client(session, client_data):
    crud = CRUDMixin(session)
    client = crud.create(Client, **client_data)
    deleted_client = crud.delete(Client, client.id)
    assert deleted_client is not None
    deleted_client_check = session.query(Client).filter_by(id=client.id).first()
    assert deleted_client_check is None


def test_list_clients(session, client_data):
    crud = CRUDMixin(session)
    crud.create(Client, **client_data)
    crud.create(
        Client,
        name="Client 2",
        email="client2@example.com",
        phone="0600000000",
        company="Company2",
        contact_commercial_id=1,
    )
    clients = crud.list(Client)
    assert len(clients) >= 2
    assert any(c.email == "user1@example.com" for c in clients)
    assert any(c.email == "client2@example.com" for c in clients)
