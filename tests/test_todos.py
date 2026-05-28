import pytest
from app.models import Todo

# Helper to register and login a user, returning their headers
def get_user_headers(client, email, name="Test User"):
    response = client.post(
        "/register",
        json={"name": name, "email": email, "password": "password123"},
    )
    token = response.json()["token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_todo_success(client):
    headers = get_user_headers(client, "user@test.com")
    payload = {"title": "Buy milk", "description": "Whole milk and organic eggs"}

    response = client.post("/todos/", json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "Buy milk"
    assert data["description"] == "Whole milk and organic eggs"
    assert data["completed"] is False


def test_create_todo_unauthorized(client):
    # No Auth headers
    response = client.post("/todos/", json={"title": "Buy milk"})
    assert response.status_code == 401
    assert "Unauthorized" in response.json()["detail"]


def test_get_todos_isolation(client):
    headers_u1 = get_user_headers(client, "u1@test.com", "User One")
    headers_u2 = get_user_headers(client, "u2@test.com", "User Two")

    # Create todo for User 1
    client.post("/todos/", json={"title": "Task User 1"}, headers=headers_u1)

    # Create todo for User 2
    client.post("/todos/", json={"title": "Task User 2"}, headers=headers_u2)

    # User 1 fetches
    res_u1 = client.get("/todos/", headers=headers_u1)
    assert res_u1.status_code == 200
    data_u1 = res_u1.json()
    assert data_u1["total"] == 1
    assert data_u1["data"][0]["title"] == "Task User 1"

    # User 2 fetches
    res_u2 = client.get("/todos/", headers=headers_u2)
    assert res_u2.status_code == 200
    data_u2 = res_u2.json()
    assert data_u2["total"] == 1
    assert data_u2["data"][0]["title"] == "Task User 2"


def test_get_todos_pagination(client):
    headers = get_user_headers(client, "user@test.com")

    # Seed 5 tasks
    for i in range(5):
        client.post("/todos/", json={"title": f"Task {i}"}, headers=headers)

    # Page 1, limit 2
    response = client.get("/todos/?page=1&limit=2", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["page"] == 1
    assert data["limit"] == 2
    assert len(data["data"]) == 2
    assert data["total"] == 5


def test_get_todos_completed_filter(client):
    headers = get_user_headers(client, "user@test.com")

    # Create active todo
    res1 = client.post("/todos/", json={"title": "Task Active"}, headers=headers)
    todo_active_id = res1.json()["id"]

    # Create completed todo
    res2 = client.post("/todos/", json={"title": "Task Completed"}, headers=headers)
    todo_comp_id = res2.json()["id"]
    client.put(f"/todos/{todo_comp_id}", json={"completed": True}, headers=headers)

    # Filter by completed = True
    response = client.get("/todos/?completed=true", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["data"][0]["title"] == "Task Completed"


def test_get_todos_search(client):
    headers = get_user_headers(client, "user@test.com")

    client.post("/todos/", json={"title": "Apple juice", "description": "Organic"}, headers=headers)
    client.post("/todos/", json={"title": "Orange juice", "description": "Tropicana"}, headers=headers)

    response = client.get("/todos/?search=Apple", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["data"][0]["title"] == "Apple juice"


def test_update_todo_success(client):
    headers = get_user_headers(client, "user@test.com")
    res = client.post("/todos/", json={"title": "Old title"}, headers=headers)
    todo_id = res.json()["id"]

    # Update
    response = client.put(
        f"/todos/{todo_id}",
        json={"title": "New title", "completed": True},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New title"
    assert data["completed"] is True


def test_update_todo_unauthorized(client):
    headers_u1 = get_user_headers(client, "u1@test.com")
    headers_u2 = get_user_headers(client, "u2@test.com")

    # User 1 creates todo
    res = client.post("/todos/", json={"title": "U1 Todo"}, headers=headers_u1)
    todo_id = res.json()["id"]

    # User 2 attempts to update User 1's todo
    response = client.put(
        f"/todos/{todo_id}", json={"title": "Hacked Title"}, headers=headers_u2
    )
    assert response.status_code == 403
    assert "Forbidden" in response.json()["detail"]


def test_update_todo_not_found(client):
    headers = get_user_headers(client, "user@test.com")
    response = client.put(
        "/todos/non-existent-uuid",
        json={"title": "Hacked Title"},
        headers=headers,
    )
    assert response.status_code == 404


def test_delete_todo_success(client, db):
    headers = get_user_headers(client, "user@test.com")
    res = client.post("/todos/", json={"title": "Delete me"}, headers=headers)
    todo_id = res.json()["id"]

    # Delete
    response = client.delete(f"/todos/{todo_id}", headers=headers)
    assert response.status_code == 204

    # Verify deleted
    verify = client.get("/todos/", headers=headers)
    assert verify.json()["total"] == 0


def test_delete_todo_unauthorized(client):
    headers_u1 = get_user_headers(client, "u1@test.com")
    headers_u2 = get_user_headers(client, "u2@test.com")

    # User 1 creates
    res = client.post("/todos/", json={"title": "U1 Todo"}, headers=headers_u1)
    todo_id = res.json()["id"]

    # User 2 attempts delete
    response = client.delete(f"/todos/{todo_id}", headers=headers_u2)
    assert response.status_code == 403
