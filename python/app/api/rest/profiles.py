from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.application.dto.profile_dto import ProfileData
from app.application.services.profile_query_service import ProfileQueryService
from app.core.repositories.user_repository import UserRepository
from app.core.domain.follow import FollowRelation
from app.api.dependencies import (
    get_profile_query_service,
    get_user_repository,
    get_current_user_id,
    get_current_user_id_required
)

router = APIRouter()


class ProfileResponse(BaseModel):
    profile: ProfileData


@router.get("/profiles/{username}", response_model=ProfileResponse)
def get_profile(
    username: str,
    current_user_id: Optional[str] = Depends(get_current_user_id),
    profile_query_service: ProfileQueryService = Depends(get_profile_query_service)
):
    profile = profile_query_service.find_by_username(username, current_user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return ProfileResponse(profile=profile)


@router.post("/profiles/{username}/follow", response_model=ProfileResponse)
def follow_user(
    username: str,
    current_user_id: str = Depends(get_current_user_id_required),
    user_repository: UserRepository = Depends(get_user_repository),
    profile_query_service: ProfileQueryService = Depends(get_profile_query_service)
):
    user_to_follow = user_repository.find_by_username(username)
    if not user_to_follow:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_to_follow.id == current_user_id:
        raise HTTPException(status_code=422, detail="Cannot follow yourself")
    
    existing_relation = user_repository.find_relation(current_user_id, user_to_follow.id)
    if not existing_relation:
        relation = FollowRelation(user_id=current_user_id, follow_id=user_to_follow.id)
        user_repository.save_relation(relation)
    
    profile = profile_query_service.find_by_username(username, current_user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return ProfileResponse(profile=profile)


@router.delete("/profiles/{username}/follow", response_model=ProfileResponse)
def unfollow_user(
    username: str,
    current_user_id: str = Depends(get_current_user_id_required),
    user_repository: UserRepository = Depends(get_user_repository),
    profile_query_service: ProfileQueryService = Depends(get_profile_query_service)
):
    user_to_unfollow = user_repository.find_by_username(username)
    if not user_to_unfollow:
        raise HTTPException(status_code=404, detail="User not found")
    
    relation = FollowRelation(user_id=current_user_id, follow_id=user_to_unfollow.id)
    user_repository.remove_relation(relation)
    
    profile = profile_query_service.find_by_username(username, current_user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return ProfileResponse(profile=profile)
