from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.core.config import settings
from app.core.security import verify_password, get_password_hash, create_access_token
from app.schemas.schemas import UserCreate, UserResponse, Token, UserLogin
from app.models.models import UserModel
from app.utils.database import DatabaseUtils

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    """Register a new user"""
    # Check if user already exists
    existing_user = await DatabaseUtils.find_one(
        UserModel.collection_name,
        {"email": user.email}
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create new user
    hashed_password = get_password_hash(user.password)
    user_data = {
        "email": user.email,
        "full_name": user.full_name,
        "hashed_password": hashed_password,
        "role": user.role,
        "is_active": True
    }

    user_model = UserModel(**user_data)
    result = await DatabaseUtils.create(UserModel.collection_name, user_model.to_dict())

    return UserResponse(
        id=str(result.inserted_id),
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        is_active=True
    )

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate user and return access token"""
    user = await DatabaseUtils.find_one(
        UserModel.collection_name,
        {"email": form_data.username}
    )

    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user["_id"])}, expires_delta=access_token_expires
    )

    # Update last login
    await DatabaseUtils.update_by_id(
        UserModel.collection_name,
        str(user["_id"]),
        {"last_login": "utcnow()"}
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login-json", response_model=Token)
async def login_json(user_login: UserLogin):
    """JSON-based login endpoint"""
    user = await DatabaseUtils.find_one(
        UserModel.collection_name,
        {"email": user_login.email}
    )

    if not user or not verify_password(user_login.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user["_id"])}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}