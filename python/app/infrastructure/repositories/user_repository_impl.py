from typing import Optional
from sqlalchemy.orm import Session
from app.core.domain.user import User
from app.core.domain.follow import FollowRelation
from app.core.repositories.user_repository import UserRepository
from app.infrastructure.db.models import UserModel, FollowModel


class UserRepositoryImpl(UserRepository):
    def __init__(self, db: Session):
        self.db = db
    
    def save(self, user: User) -> User:
        user_model = self.db.query(UserModel).filter(UserModel.id == user.id).first()
        if user_model:
            user_model.username = user.username
            user_model.email = user.email
            user_model.password = user.password
            user_model.bio = user.bio
            user_model.image = user.image
        else:
            user_model = UserModel(
                id=user.id,
                username=user.username,
                email=user.email,
                password=user.password,
                bio=user.bio,
                image=user.image
            )
            self.db.add(user_model)
        self.db.commit()
        self.db.refresh(user_model)
        return self._to_domain(user_model)
    
    def find_by_id(self, user_id: str) -> Optional[User]:
        user_model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_domain(user_model) if user_model else None
    
    def find_by_email(self, email: str) -> Optional[User]:
        user_model = self.db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_domain(user_model) if user_model else None
    
    def find_by_username(self, username: str) -> Optional[User]:
        user_model = self.db.query(UserModel).filter(UserModel.username == username).first()
        return self._to_domain(user_model) if user_model else None
    
    def save_relation(self, relation: FollowRelation) -> None:
        follow_model = FollowModel(user_id=relation.user_id, follow_id=relation.follow_id)
        self.db.add(follow_model)
        self.db.commit()
    
    def remove_relation(self, relation: FollowRelation) -> None:
        self.db.query(FollowModel).filter(
            FollowModel.user_id == relation.user_id,
            FollowModel.follow_id == relation.follow_id
        ).delete()
        self.db.commit()
    
    def find_relation(self, user_id: str, follow_id: str) -> Optional[FollowRelation]:
        follow_model = self.db.query(FollowModel).filter(
            FollowModel.user_id == user_id,
            FollowModel.follow_id == follow_id
        ).first()
        return FollowRelation(user_id=user_id, follow_id=follow_id) if follow_model else None
    
    def _to_domain(self, user_model: UserModel) -> User:
        return User(
            id=user_model.id,
            username=user_model.username,
            email=user_model.email,
            password=user_model.password,
            bio=user_model.bio,
            image=user_model.image
        )
