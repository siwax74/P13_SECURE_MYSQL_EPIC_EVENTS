from app.mixins import CRUDMixin
from app.models.user import User


def test_create_user(session, user_data):
    crud = CRUDMixin(session)
    user = crud.create(User, **user_data)
    assert user is not None
    for key, value in user_data.items():
        assert getattr(user, key) == value


def test_update_user(session, user_data):
    crud = CRUDMixin(session)
    user = crud.create(User, **user_data)
    updated_user = crud.update(User, user.id, username="updateduser")
    assert updated_user.username == "updateduser"


def test_delete_user(session, user_data):
    crud = CRUDMixin(session)
    user = crud.create(User, **user_data)
    deleted_user = crud.delete(User, user.id)
    assert deleted_user is not None
    deleted_user_check = session.query(User).filter_by(id=user.id).first()
    assert deleted_user_check is None


def test_list_users(session, user_data):
    crud = CRUDMixin(session)
    crud.create(User, **user_data)
    crud.create(
        User, username="user2", email="user2@example.com", password_hash="hashed_password2", is_commercial=True
    )
    users = crud.list(User)
    assert len(users) >= 2
    assert any(u.email == "user@example.com" for u in users)
    assert any(u.email == "user2@example.com" for u in users)
