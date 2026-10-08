from fastapi.testclient import TestClient
from app.main import app, syntax_check

client = TestClient(app)


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_valid_syntax():
    assert syntax_check("x = 1") is None


def test_invalid_syntax():
    issue = syntax_check("def bad(:\n pass")
    assert issue is not None
    assert issue.severity == "high"


def test_review_syntax_error_without_api():
    response = client.post("/review", json={"code": "def bad(:\n pass"})
    assert response.status_code == 200
    assert response.json()["issues"][0]["severity"] == "high"


def test_empty_code_rejected():
    assert client.post("/review", json={"code": ""}).status_code == 422
