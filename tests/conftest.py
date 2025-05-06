# tests/conftest.py
from datetime import datetime, timedelta
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base


@pytest.fixture(scope="function")
def session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def client_data():
    client_data = {
        "name": "test_client",
        "email": "user1@example.com",
        "phone": "0611192701",
        "company": "LeDuc",
        "contact_commercial_id": 1,
    }
    return client_data


@pytest.fixture
def contract_data():
    contract_data = {
        "client_id": 1,
        "contact_commercial_id": 1,
        "total_amount": 10000.0,
        "remaining_amount": 4000.0,
        "signed": False,
    }
    return contract_data


@pytest.fixture
def user_data():
    user_data = {
        "username": "testuser",
        "email": "user@example.com",
        "password_hash": "hashed_password",
        "is_support": False,
        "is_commercial": True,
        "is_management": False,
    }
    return user_data


@pytest.fixture
def event_data():
    event_data = {
        "title": "Conférence annuelle",
        "contract_id": 1,
        "client_id": 1,
        "support_contact_id": 1,
        "start_datetime": datetime.now() + timedelta(days=1),
        "end_datetime": datetime.now() + timedelta(days=1, hours=2),
        "location": "Paris, Salle 402",
        "attendees": 50,
        "notes": "Prévoir matériel de présentation",
    }
    return event_data
