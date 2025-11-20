import pytest


def create_user_and_get_token(client, email="test@example.com", username="testuser"):
    response = client.post(
        "/api/users",
        json={
            "user": {
                "email": email,
                "username": username,
                "password": "password123"
            }
        }
    )
    return response.json()["user"]["token"]


def test_create_article(client):
    token = create_user_and_get_token(client)
    
    response = client.post(
        "/api/articles",
        json={
            "article": {
                "title": "Test Article",
                "description": "Test Description",
                "body": "Test Body",
                "tag_list": ["python", "testing"]
            }
        },
        headers={"Authorization": f"Token {token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "article" in data
    assert data["article"]["title"] == "Test Article"
    assert data["article"]["slug"] == "test-article"
    assert len(data["article"]["tag_list"]) == 2


def test_get_articles(client):
    token = create_user_and_get_token(client)
    
    client.post(
        "/api/articles",
        json={
            "article": {
                "title": "Test Article",
                "description": "Test Description",
                "body": "Test Body",
                "tag_list": ["python"]
            }
        },
        headers={"Authorization": f"Token {token}"}
    )
    
    response = client.get("/api/articles")
    
    assert response.status_code == 200
    data = response.json()
    assert "articles" in data
    assert "articles_count" in data
    assert len(data["articles"]) == 1


def test_get_article_by_slug(client):
    token = create_user_and_get_token(client)
    
    client.post(
        "/api/articles",
        json={
            "article": {
                "title": "Test Article",
                "description": "Test Description",
                "body": "Test Body",
                "tag_list": []
            }
        },
        headers={"Authorization": f"Token {token}"}
    )
    
    response = client.get("/api/articles/test-article")
    
    assert response.status_code == 200
    data = response.json()
    assert "article" in data
    assert data["article"]["slug"] == "test-article"


def test_update_article(client):
    token = create_user_and_get_token(client)
    
    client.post(
        "/api/articles",
        json={
            "article": {
                "title": "Original Title",
                "description": "Original Description",
                "body": "Original Body",
                "tag_list": []
            }
        },
        headers={"Authorization": f"Token {token}"}
    )
    
    response = client.put(
        "/api/articles/original-title",
        json={
            "article": {
                "title": "Updated Title"
            }
        },
        headers={"Authorization": f"Token {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["article"]["title"] == "Updated Title"
    assert data["article"]["slug"] == "updated-title"


def test_delete_article(client):
    token = create_user_and_get_token(client)
    
    client.post(
        "/api/articles",
        json={
            "article": {
                "title": "Test Article",
                "description": "Test Description",
                "body": "Test Body",
                "tag_list": []
            }
        },
        headers={"Authorization": f"Token {token}"}
    )
    
    response = client.delete(
        "/api/articles/test-article",
        headers={"Authorization": f"Token {token}"}
    )
    
    assert response.status_code == 204
    
    get_response = client.get("/api/articles/test-article")
    assert get_response.status_code == 404
