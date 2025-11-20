import pytest


def test_get_tags(client):
    response = client.get("/api/tags")
    
    assert response.status_code == 200
    data = response.json()
    assert "tags" in data
    assert isinstance(data["tags"], list)
