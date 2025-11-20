import pytest


def test_create_user(client):
    response = client.post(
        "/api/users",
        json={
            "user": {
                "email": "test@example.com",
                "username": "testuser",
                "password": "password123"
            }
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "user" in data
    assert data["user"]["email"] == "test@example.com"
    assert data["user"]["username"] == "testuser"
    assert "token" in data["user"]


def test_create_user_duplicate_email(client):
    client.post(
        "/api/users",
        json={
            "user": {
                "email": "test@example.com",
                "username": "testuser1",
                "password": "password123"
            }
        }
    )
    
    response = client.post(
        "/api/users",
        json={
            "user": {
                "email": "test@example.com",
                "username": "testuser2",
                "password": "password123"
            }
        }
    )
    
    assert response.status_code == 422


def test_login_user(client):
    client.post(
        "/api/users",
        json={
            "user": {
                "email": "test@example.com",
                "username": "testuser",
                "password": "password123"
            }
        }
    )
    
    response = client.post(
        "/api/users/login",
        json={
            "user": {
                "email": "test@example.com",
                "password": "password123"
            }
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "user" in data
    assert data["user"]["email"] == "test@example.com"
    assert "token" in data["user"]


def test_login_user_invalid_credentials(client):
    response = client.post(
        "/api/users/login",
        json={
            "user": {
                "email": "nonexistent@example.com",
                "password": "wrongpassword"
            }
        }
    )
    
    assert response.status_code == 401
