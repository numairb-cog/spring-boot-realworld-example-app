from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.application.dto.user_dto import RegisterParam, LoginParam, UserWithToken
from app.application.services.user_service import UserService
from app.application.services.user_query_service import UserQueryService
from app.core.repositories.user_repository import UserRepository
from app.infrastructure.security.jwt_service import JwtService
from app.infrastructure.security.password_hasher import PasswordHasher
from app.api.dependencies import (
    get_user_service,
    get_user_query_service,
    get_user_repository,
    get_jwt_service,
    get_password_hasher
)

router = APIRouter()


class UserRequest(BaseModel):
    user: RegisterParam


class LoginRequest(BaseModel):
    user: LoginParam


class UserResponse(BaseModel):
    user: UserWithToken


@router.post("/users", response_model=UserResponse, status_code=201)
def create_user(
    request: UserRequest,
    user_service: UserService = Depends(get_user_service),
    user_query_service: UserQueryService = Depends(get_user_query_service),
    jwt_service: JwtService = Depends(get_jwt_service)
):
    try:
        user = user_service.create_user(request.user)
        user_data = user_query_service.find_by_id(user.id)
        if not user_data:
            raise HTTPException(status_code=500, detail="Failed to retrieve user data")
        
        token = jwt_service.to_token(user)
        user_with_token = UserWithToken(
            email=user_data.email,
            username=user_data.username,
            bio=user_data.bio,
            image=user_data.image,
            token=token
        )
        return UserResponse(user=user_with_token)
    except ValueError as e:
        raise HTTPException(status_code=422, detail={"errors": {"body": [str(e)]}})


@router.post("/users/login", response_model=UserResponse)
def login_user(
    request: LoginRequest,
    user_repository: UserRepository = Depends(get_user_repository),
    user_query_service: UserQueryService = Depends(get_user_query_service),
    jwt_service: JwtService = Depends(get_jwt_service),
    password_hasher: PasswordHasher = Depends(get_password_hasher)
):
    user = user_repository.find_by_email(request.user.email)
    
    if not user or not password_hasher.verify(request.user.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    user_data = user_query_service.find_by_id(user.id)
    if not user_data:
        raise HTTPException(status_code=500, detail="Failed to retrieve user data")
    
    token = jwt_service.to_token(user)
    user_with_token = UserWithToken(
        email=user_data.email,
        username=user_data.username,
        bio=user_data.bio,
        image=user_data.image,
        token=token
    )
    return UserResponse(user=user_with_token)
