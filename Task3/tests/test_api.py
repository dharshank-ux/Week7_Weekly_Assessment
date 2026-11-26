from fastapi.testclient import TestClient

from Task3.src import api


client = TestClient(api.app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "RAG API is running"


def test_valid_api_key(monkeypatch):
    monkeypatch.setattr(
        api,
        "answer",
        lambda question, k=4: "You get 12 casual leaves per year."
    )

    response = client.post(
        "/ask",
        headers={"x-api-key": "week7-local-secret-key"},
        json={"question": "How many casual leaves?"}
    )

    assert response.status_code == 200
    assert "12 casual leaves" in response.json()["answer"]


def test_invalid_api_key():
    response = client.post(
        "/ask",
        headers={"x-api-key": "wrong-key"},
        json={"question": "How many casual leaves?"}
    )

    assert response.status_code == 401


def test_missing_api_key():
    response = client.post(
        "/ask",
        json={"question": "How many casual leaves?"}
    )

    assert response.status_code == 401


def test_no_results(monkeypatch):
    monkeypatch.setattr(
        api,
        "answer",
        lambda question, k=4: "I don't have information on that"
    )

    response = client.post(
        "/ask",
        headers={"x-api-key": "week7-local-secret-key"},
        json={"question": "Who is the CEO?"}
    )

    assert response.status_code == 404


def test_empty_question():
    response = client.post(
        "/ask",
        headers={"x-api-key": "week7-local-secret-key"},
        json={"question": "   "}
    )

    assert response.status_code == 400