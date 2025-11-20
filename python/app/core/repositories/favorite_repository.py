from abc import ABC, abstractmethod
from typing import Optional
from app.core.domain.favorite import ArticleFavorite


class FavoriteRepository(ABC):
    @abstractmethod
    def save(self, favorite: ArticleFavorite) -> None:
        pass
    
    @abstractmethod
    def remove(self, favorite: ArticleFavorite) -> None:
        pass
    
    @abstractmethod
    def find(self, user_id: str, article_id: str) -> Optional[ArticleFavorite]:
        pass
