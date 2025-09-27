
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from jose import JWTError, jwt
from ..core.config import settings
from ..models.models import UserModel, UserRole
from ..schemas.schemas import UserCreate
from ..utils.database import DatabaseUtils

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db):
        self.db = db

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)

    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email from database"""
        users = await DatabaseUtils.find_many(
            UserModel.collection_name, 
            {"email": email}, 
            1
        )
        return users[0] if users else None

    async def authenticate_user(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate a user"""
        user = await self.get_user_by_email(email)
        if not user:
            return None
        if not self.verify_password(password, user["hashed_password"]):
            return None
        if not user.get("is_active", True):
            return None
        
        # Update last login
        await DatabaseUtils.update_one(
            UserModel.collection_name,
            user["id"],
            {"last_login": datetime.utcnow()}
        )
        
        return user

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        """Create JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt

    async def get_current_user(self, token: str) -> Optional[Dict[str, Any]]:
        """Get current user from JWT token"""
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            email: str = payload.get("sub")
            if email is None:
                return None
        except JWTError:
            return None
        
        user = await self.get_user_by_email(email)
        return user

    async def create_user(self, user_data: UserCreate) -> Dict[str, Any]:
        """Create a new user"""
        # Check if user already exists
        existing_user = await self.get_user_by_email(user_data.email)
        if existing_user:
            raise ValueError("Email already registered")

        # Hash password
        hashed_password = self.get_password_hash(user_data.password)
        
        # Create user document
        user_dict = {
            "email": user_data.email,
            "full_name": user_data.full_name,
            "hashed_password": hashed_password,
            "role": user_data.role,
            "is_active": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        # Insert user
        user_id = await DatabaseUtils.insert_one(UserModel.collection_name, user_dict)
        if not user_id:
            raise ValueError("Failed to create user")
        
        # Return created user (without password)
        created_user = await DatabaseUtils.find_by_id(UserModel.collection_name, user_id)
        created_user.pop("hashed_password", None)
        return created_user
