from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.application.dto.article_dto import ArticleData
from app.application.services.article_query_service import ArticleQueryService
from app.core.repositories.article_repository import ArticleRepository
from app.core.repositories.favorite_repository import FavoriteRepository
from app.core.domain.favorite import ArticleFavorite
from app.api.dependencies import (
    get_article_query_service,
    get_article_repository,
    get_favorite_repository,
    get_current_user_id_required
)

router = APIRouter()


class ArticleResponse(BaseModel):
    article: ArticleData


@router.post("/articles/{slug}/favorite", response_model=ArticleResponse)
def favorite_article(
    slug: str,
    current_user_id: str = Depends(get_current_user_id_required),
    article_repository: ArticleRepository = Depends(get_article_repository),
    favorite_repository: FavoriteRepository = Depends(get_favorite_repository),
    article_query_service: ArticleQueryService = Depends(get_article_query_service)
):
    article = article_repository.find_by_slug(slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    existing_favorite = favorite_repository.find(current_user_id, article.id)
    if not existing_favorite:
        favorite = ArticleFavorite(user_id=current_user_id, article_id=article.id)
        favorite_repository.save(favorite)
    
    article_data = article_query_service.find_by_slug(slug, current_user_id)
    if not article_data:
        raise HTTPException(status_code=500, detail="Failed to retrieve article data")
    return ArticleResponse(article=article_data)


@router.delete("/articles/{slug}/favorite", response_model=ArticleResponse)
def unfavorite_article(
    slug: str,
    current_user_id: str = Depends(get_current_user_id_required),
    article_repository: ArticleRepository = Depends(get_article_repository),
    favorite_repository: FavoriteRepository = Depends(get_favorite_repository),
    article_query_service: ArticleQueryService = Depends(get_article_query_service)
):
    article = article_repository.find_by_slug(slug)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    favorite = ArticleFavorite(user_id=current_user_id, article_id=article.id)
    favorite_repository.remove(favorite)
    
    article_data = article_query_service.find_by_slug(slug, current_user_id)
    if not article_data:
        raise HTTPException(status_code=500, detail="Failed to retrieve article data")
    return ArticleResponse(article=article_data)
