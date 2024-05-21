import pytest
from fastapi.testclient import TestClient
from main2 import app, UserModel, SessionModel, MessageModel

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_user():
    user = UserModel(username="testuser", email="testuser@example.com")
    response = client.post("/users", json=user.dict())
    assert response.status_code == 200
    assert "user_id" in response.json()

def test_read_user():
    # Assuming a user with id 'test_id' exists
    response = client.get("/users/test_id")
    assert response.status_code == 200
    assert "username" in response.json()

def test_create_session():
    # Assuming a user with id 'test_id' exists
    session = SessionModel(user_id="test_id")
    response = client.post("/createSession", json=session.dict())
    assert response.status_code == 200
    assert "session_id" in response.json()

def test_get_session():
    # Assuming a session with id 'test_session_id' exists
    response = client.get("/sessions/test_session_id")
    assert response.status_code == 200
    assert "session" in response.json()

def test_get_session_list():
    # Assuming a user with id 'test_id' exists
    response = client.get("/users/test_id/sessions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_message():
    # Assuming a session with id 'test_session_id' exists
    message = MessageModel(session_id="test_session_id", user_id="test_id", message_text="Hello", is_bot=False)
    response = client.post("/messages", json=message.dict())
    assert response.status_code == 200
    assert "message_id" in response.json()