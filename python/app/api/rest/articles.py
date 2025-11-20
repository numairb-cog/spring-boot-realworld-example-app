from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from app.application.dto.article_dto import NewArticleParam, UpdateArticleParam, ArticleData, ArticleDataList, Page
from app.application.services.article_service import ArticleCommandService
from app.application.services.article_query_service import ArticleQueryService
from app.core.repositories.user_repository import UserRepository
from app.api.dependencies import (
    get_article_command_service,
    get_article_query_service,
    get_current_user_id,
    get_current_user_id_required,
    get_user_repository
)

router = APIRouter()


class NewArticleRequest(BaseModel):
    article: NewArticleParam


class UpdateArticleRequest(BaseModel):
    article: UpdateArticleParam


class ArticleResponse(BaseModel):
    article: ArticleData


class ArticlesResponse(BaseModel):
    articles: list[ArticleData]
    articles_count: int


@router.post("/articles", response_model=ArticleResponse, status_code=201)
def create_article(
    request: NewArticleRequest,
    current_user_id: str = Depends(get_current_user_id_required),
    article_service: ArticleCommandService = Depends(get_article_command_service),
    article_query_service: ArticleQueryService = Depends(get_article_query_service)
):
    article = article_service.create_article(request.article, current_user_id)
    article_data = article_query_service.find_by_slug(article.slug, current_user_id)
    if not article_data:
        raise HTTPException(status_code=500, detail="Failed to retrieve article data")
    return ArticleResponse(article=article_data)


@router.get("/articles", response_model=ArticlesResponse)
def get_articles(
    tag: Optional[str] = Query(None),
    author: Optional[str] = Query(None),
    favorited: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user_id: Optional[str] = Depends(get_current_user_id),
    article_query_service: ArticleQueryService = Depends(get_article_query_service)
):
    page = Page(offset=offset, limit=limit)
    result = article_query_service.find_recent_articles(
        page=page,
        tag=tag,
        author=author,
        favorited=favorited,
        current_user_id=current_user_id
    )
    return ArticlesResponse(articles=result.articles, articles_count=result.articles_count)


@router.get("/articles/feed", response_model=ArticlesResponse)
def get_feed(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user_id: str = Depends(get_current_user_id_required),
    article_query_service: ArticleQueryService = Depends(get_article_query_service)
):
    page = Page(offset=offset, limit=limit)
    result = article_query_service.find_user_feed(current_user_id, page)
    return ArticlesResponse(articles=result.articles, articles_count=result.articles_count)


@router.get("/articles/{slug}", response_model=ArticleResponse)
def get_article(
    slug: str,
    current_user_id: Optional[str] = Depends(get_current_user_id),
    article_query_service: ArticleQueryService = Depends(get_article_query_service)
):
    article_data = article_query_service.find_by_slug(slug, current_user_id)
    if not article_data:
        raise HTTPException(status_code=404, detail="Article not found")
    return ArticleResponse(article=article_data)


@router.put("/articles/{slug}", response_model=ArticleResponse)
def update_article(
    slug: str,
    request: UpdateArticleRequest,
    current_user_id: str = Depends(get_current_user_id_required),
    article_service: ArticleCommandService = Depends(get_article_command_service),
    article_query_service: ArticleQueryService = Depends(get_article_query_service),
    user_repository: UserRepository = Depends(get_user_repository)
):
    existing_article = article_query_service.find_by_slug(slug, current_user_id)
    if not existing_article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    user = user_repository.find_by_id(current_user_id)
    if not user or user.username != existing_article.author.username:
        raise HTTPException(status_code=403, detail="Not authorized to update this article")
    
    article = article_service.update_article(slug, request.article)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    article_data = article_query_service.find_by_slug(article.slug, current_user_id)
    if not article_data:
        raise HTTPException(status_code=500, detail="Failed to retrieve article data")
    return ArticleResponse(article=article_data)


@router.delete("/articles/{slug}", status_code=204)
def delete_article(
    slug: str,
    current_user_id: str = Depends(get_current_user_id_required),
    article_service: ArticleCommandService = Depends(get_article_command_service),
    article_query_service: ArticleQueryService = Depends(get_article_query_service)
):
    existing_article = article_query_service.find_by_slug(slug, current_user_id)
    if not existing_article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    success = article_service.delete_article(slug)
    if not success:
        raise HTTPException(status_code=404, detail="Article not found")
    return None
