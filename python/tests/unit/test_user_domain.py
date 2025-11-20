import pytest
from app.core.domain.user import User


def test_user_creation():
    user = User(
        email="test@example.com",
        username="testuser",
        password="hashedpassword"
    )
    assert user.email == "test@example.com"
    assert user.username == "testuser"
    assert user.password == "hashedpassword"
    assert user.id is not None


def test_user_update():
    user = User(
        email="test@example.com",
        username="testuser",
        password="hashedpassword"
    )
    
    user.update(email="newemail@example.com", username="newusername")
    assert user.email == "newemail@example.com"
    assert user.username == "newusername"


def test_user_update_with_empty_values():
    user = User(
        email="test@example.com",
        username="testuser",
        password="hashedpassword"
    )
    
    user.update(email="", username="")
    assert user.email == "test@example.com"
    assert user.username == "testuser"
