from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_and_read_snippet():
    # 1) Yeni bir snippet oluştur
    yeni = {
        "title": "Test snippet",
        "language": "python",
        "body": "print('test')",
        "tags": ["test", "python"],
    }
    post_response = client.post("/snippets", json=yeni)
    assert post_response.status_code == 200

    # 2) Dönen cevabı kontrol et
    olusan = post_response.json()
    assert olusan["title"] == "Test snippet"
    assert sorted(olusan["tags"]) == ["python", "test"]
    snippet_id = olusan["id"]

    # 3) Aynı snippet'i tekil GET ile geri oku
    get_response = client.get(f"/snippets/{snippet_id}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Test snippet"    
