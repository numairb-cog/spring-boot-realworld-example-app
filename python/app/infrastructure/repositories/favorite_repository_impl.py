from typing import Optional
from sqlalchemy.orm import Session
from app.core.domain.favorite import ArticleFavorite
from app.core.repositories.favorite_repository import FavoriteRepository
from app.infrastructure.db.models import ArticleFavoriteModel


class FavoriteRepositoryImpl(FavoriteRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def save(self, favorite: ArticleFavorite) -> None:
        favorite_model = ArticleFavoriteModel(
            user_id=favorite.user_id,
            article_id=favorite.article_id
        )
        self.db.add(favorite_model)
        self.db.commit()
    
    def remove(self, favorite: ArticleFavorite) -> None:
        self.db.query(ArticleFavoriteModel).filter(
            ArticleFavoriteModel.user_id == favorite.user_id,
            ArticleFavoriteModel.article_id == favorite.article_id
        ).delete()
        self.db.commit()
    
    def find(self, user_id: str, article_id: str) -> Optional[ArticleFavorite]:
        favorite_model = self.db.query(ArticleFavoriteModel).filter(
            ArticleFavoriteModel.user_id == user_id,
            ArticleFavoriteModel.article_id == article_id
        ).first()
        return ArticleFavorite(user_id=user_id, article_id=article_id) if favorite_model else None
