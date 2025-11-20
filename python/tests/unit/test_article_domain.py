import pytest
from app.core.domain.article import Article, Tag


def test_article_creation():
    tags = [Tag(name="python"), Tag(name="testing")]
    article = Article(
        title="Test Article",
        description="Test Description",
        body="Test Body",
        user_id="user123",
        tags=tags
    )
    
    assert article.title == "Test Article"
    assert article.description == "Test Description"
    assert article.body == "Test Body"
    assert article.user_id == "user123"
    assert len(article.tags) == 2
    assert article.slug == "test-article"


def test_article_slug_generation():
    slug = Article.to_slug("How to Train Your Dragon")
    assert slug == "how-to-train-your-dragon"


def test_article_update():
    tags = [Tag(name="python")]
    article = Article(
        title="Original Title",
        description="Original Description",
        body="Original Body",
        user_id="user123",
        tags=tags
    )
    
    original_slug = article.slug
    article.update(title="Updated Title")
    
    assert article.title == "Updated Title"
    assert article.slug != original_slug
    assert article.slug == "updated-title"


def test_article_update_with_empty_values():
    tags = [Tag(name="python")]
    article = Article(
        title="Original Title",
        description="Original Description",
        body="Original Body",
        user_id="user123",
        tags=tags
    )
    
    article.update(title="", description="", body="")
    assert article.title == "Original Title"
    assert article.description == "Original Description"
    assert article.body == "Original Body"
