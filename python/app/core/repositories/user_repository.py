from abc import ABC, abstractmethod
from typing import Optional
from app.core.domain.user import User
from app.core.domain.follow import FollowRelation


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> User:
        pass
    
    @abstractmethod
    def find_by_id(self, user_id: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def find_by_username(self, username: str) -> Optional[User]:
        pass
    
    @abstractmethod
    def save_relation(self, relation: FollowRelation) -> None:
        pass
    
    @abstractmethod
    def remove_relation(self, relation: FollowRelation) -> None:
        pass
    
    @abstractmethod
    def find_relation(self, user_id: str, follow_id: str) -> Optional[FollowRelation]:
        pass
