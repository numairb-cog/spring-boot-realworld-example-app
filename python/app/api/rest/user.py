from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.application.dto.user_dto import UpdateUserParam, UserWithToken
from app.application.services.user_service import UserService
from app.application.services.user_query_service import UserQueryService
from app.infrastructure.security.jwt_service import JwtService
from app.api.dependencies import (
    get_user_service,
    get_user_query_service,
    get_jwt_service,
    get_current_user_id_required
)

router = APIRouter()


class UpdateUserRequest(BaseModel):
    user: UpdateUserParam


class UserResponse(BaseModel):
    user: UserWithToken


@router.get("/user", response_model=UserResponse)
def get_current_user(
    current_user_id: str = Depends(get_current_user_id_required),
    user_query_service: UserQueryService = Depends(get_user_query_service),
    jwt_service: JwtService = Depends(get_jwt_service)
):
    user_data = user_query_service.find_by_id(current_user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    from app.core.domain.user import User
    user = User(id=user_data.id, email=user_data.email, username=user_data.username, password="")
    token = jwt_service.to_token(user)
    
    user_with_token = UserWithToken(
        email=user_data.email,
        username=user_data.username,
        bio=user_data.bio,
        image=user_data.image,
        token=token
    )
    return UserResponse(user=user_with_token)


@router.put("/user", response_model=UserResponse)
def update_user(
    request: UpdateUserRequest,
    current_user_id: str = Depends(get_current_user_id_required),
    user_service: UserService = Depends(get_user_service),
    user_query_service: UserQueryService = Depends(get_user_query_service),
    jwt_service: JwtService = Depends(get_jwt_service)
):
    try:
        user = user_service.update_user(current_user_id, request.user)
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
