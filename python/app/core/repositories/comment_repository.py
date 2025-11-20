from abc import ABC, abstractmethod
from typing import Optional, List
from app.core.domain.comment import Comment


class CommentRepository(ABC):
    @abstractmethod
    def save(self, comment: Comment) -> Comment:
        pass
    
    @abstractmethod
    def find_by_id(self, comment_id: str) -> Optional[Comment]:
        pass
    
    @abstractmethod
    def find_by_article_id(self, article_id: str) -> List[Comment]:
        pass
    
    @abstractmethod
    def remove(self, comment: Comment) -> None:
        pass
