import pytest
from app.models import User, RefreshToken


def test_register_user_success(client):
    payload = {
        "name": "John Doe",
        "email": "john@doe.com",
        "password": "password123",
    }
    response = client.post("/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "token" in data
    assert "refreshToken" in data
    assert isinstance(data["token"], str)


def test_register_user_duplicate_email(client):
    payload = {
        "name": "John Doe",
        "email": "john@doe.com",
        "password": "password123",
    }
    client.post("/register", json=payload)

    # Register again with same email
    response = client.post("/register", json=payload)
    assert response.status_code == 400
    assert "Email is already registered" in response.json()["detail"]


def test_register_validation_errors(client):
    # Invalid email, short password, empty name
    payload = {
        "name": "",
        "email": "not-an-email",
        "password": "123",
    }
    response = client.post("/register", json=payload)
    assert response.status_code == 400
    data = response.json()
    assert "Validation error" in data["message"]
    assert len(data["errors"]) > 0


def test_login_success(client):
    # Register user
    client.post(
        "/register",
        json={"name": "John Doe", "email": "john@doe.com", "password": "password123"},
    )

    # Login
    response = client.post(
        "/login", json={"email": "john@doe.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert "refreshToken" in data


def test_login_invalid_credentials(client):
    # Login non-existent user
    response = client.post(
        "/login", json={"email": "john@doe.com", "password": "password123"}
    )
    assert response.status_code == 401
    assert "Invalid email or password" in response.json()["detail"]


def test_token_refresh(client):
    # Register
    register_response = client.post(
        "/register",
        json={"name": "John Doe", "email": "john@doe.com", "password": "password123"},
    )
    refresh_token = register_response.json()["refreshToken"]

    # Refresh access token
    response = client.post("/refresh", json={"refreshToken": refresh_token})
    assert response.status_code == 200
    data = response.json()
    assert "token" in data


def test_token_refresh_invalid(client):
    response = client.post("/refresh", json={"refreshToken": "invalid-token-12345"})
    assert response.status_code == 401


def test_logout(client, db):
    # Register
    register_response = client.post(
        "/register",
        json={"name": "John Doe", "email": "john@doe.com", "password": "password123"},
    )
    refresh_token = register_response.json()["refreshToken"]

    # Logout
    logout_response = client.post("/logout", json={"refreshToken": refresh_token})
    assert logout_response.status_code == 204

    # Try to refresh (should fail because token is deleted)
    refresh_response = client.post("/refresh", json={"refreshToken": refresh_token})
    assert refresh_response.status_code == 401
