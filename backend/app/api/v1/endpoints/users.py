
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.schemas.schemas import UserCreate, UserUpdate, UserResponse
from app.models.models import UserModel
from app.utils.database import DatabaseUtils
from app.middleware.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user = Depends(get_current_user)
):
    """Get all users with pagination"""
    users = await DatabaseUtils.find_many(
        UserModel.collection_name,
        {},
        skip=skip,
        limit=limit
    )
    
    return [UserResponse(**user) for user in users]

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, current_user = Depends(get_current_user)):
    """Get user by ID"""
    user = await DatabaseUtils.find_by_id(UserModel.collection_name, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse(**user)
