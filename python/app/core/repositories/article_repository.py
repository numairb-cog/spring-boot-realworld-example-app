from abc import ABC, abstractmethod
from typing import Optional, List
from app.core.domain.article import Article, Tag


class ArticleRepository(ABC):
    @abstractmethod
    def save(self, article: Article) -> Article:
        pass
    
    @abstractmethod
    def find_by_id(self, article_id: str) -> Optional[Article]:
        pass
    
    @abstractmethod
    def find_by_slug(self, slug: str) -> Optional[Article]:
        pass
    
    @abstractmethod
    def remove(self, article: Article) -> None:
        pass
    
    @abstractmethod
    def find_tag(self, tag_name: str) -> Optional[Tag]:
        pass
    
    @abstractmethod
    def get_all_tags(self) -> List[str]:
        pass
