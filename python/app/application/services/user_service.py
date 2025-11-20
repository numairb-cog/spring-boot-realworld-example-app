from typing import Optional
from app.core.domain.user import User
from app.core.repositories.user_repository import UserRepository
from app.infrastructure.security.password_hasher import PasswordHasher
from app.application.dto.user_dto import RegisterParam, UpdateUserParam
from app.config import settings


class UserService:
    def __init__(self, user_repository: UserRepository, password_hasher: PasswordHasher):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
    
    def create_user(self, param: RegisterParam) -> User:
        existing_email = self.user_repository.find_by_email(param.email)
        if existing_email:
            raise ValueError("Email already exists")
        
        existing_username = self.user_repository.find_by_username(param.username)
        if existing_username:
            raise ValueError("Username already exists")
        
        hashed_password = self.password_hasher.hash(param.password)
        user = User(
            email=param.email,
            username=param.username,
            password=hashed_password,
            image=settings.default_image
        )
        return self.user_repository.save(user)
    
    def update_user(self, user_id: str, param: UpdateUserParam) -> User:
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        
        if param.email and param.email != user.email:
            existing = self.user_repository.find_by_email(param.email)
            if existing:
                raise ValueError("Email already exists")
        
        if param.username and param.username != user.username:
            existing = self.user_repository.find_by_username(param.username)
            if existing:
                raise ValueError("Username already exists")
        
        hashed_password = None
        if param.password:
            hashed_password = self.password_hasher.hash(param.password)
        
        user.update(
            email=param.email,
            username=param.username,
            password=hashed_password,
            bio=param.bio,
            image=param.image
        )
        return self.user_repository.save(user)
