"""
Authentication routes for Nexa
Handles user login, registration, and session management
"""

from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid

from ..config import get_settings
from shared.database.connection import get_db_session
from shared.database.repositories import RepositoryFactory

router = APIRouter()
security = HTTPBearer()


class LoginRequest(BaseModel):
    user_id: Optional[str] = None
    device_type: str = "web"
    device_info: Optional[dict] = None


class LoginResponse(BaseModel):
    success: bool
    user_id: str
    session_token: str
    message: str


class UserInfo(BaseModel):
    user_id: str
    is_logged_in: bool
    login_time: Optional[datetime]
    created_at: datetime


@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    db: Session = Depends(get_db_session)
):
    """
    Login or create user session
    Mirrors VocalPA LoginPreferences functionality
    """
    try:
        repos = RepositoryFactory(db)
        
        # Generate user ID if not provided
        if not request.user_id:
            request.user_id = f"user_{uuid.uuid4().hex[:8]}"
        
        # Create or update user
        user = repos.users.update_login_status(request.user_id, True)
        
        # Generate session token
        session_token = f"session_{uuid.uuid4().hex}"
        
        # Store session info in preferences
        repos.preferences.set_preference(
            request.user_id, 
            "session_token", 
            session_token
        )
        repos.preferences.set_preference(
            request.user_id, 
            "device_type", 
            request.device_type
        )
        
        if request.device_info:
            repos.preferences.set_preference(
                request.user_id, 
                "device_info", 
                request.device_info,
                "json"
            )
        
        # Log system event
        repos.system.log_event(
            "user_login",
            "auth_service",
            f"User {request.user_id} logged in from {request.device_type}",
            "info",
            request.user_id
        )
        
        return LoginResponse(
            success=True,
            user_id=request.user_id,
            session_token=session_token,
            message="Login successful"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )


@router.post("/logout")
async def logout(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db_session)
):
    """Logout user and clear session"""
    try:
        repos = RepositoryFactory(db)
        
        # Find user by session token
        # This is a simplified approach - in production, use proper JWT tokens
        user_id = None  # Would extract from token
        
        if user_id:
            # Update login status
            repos.users.update_login_status(user_id, False)
            
            # Clear session preferences
            repos.preferences.delete_preference(user_id, "session_token")
            
            # Log event
            repos.system.log_event(
                "user_logout",
                "auth_service",
                f"User {user_id} logged out",
                "info",
                user_id
            )
        
        return {"success": True, "message": "Logout successful"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Logout failed: {str(e)}"
        )


@router.get("/me", response_model=UserInfo)
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db_session)
):
    """Get current user information"""
    try:
        # In a real implementation, decode JWT token to get user_id
        # For now, we'll use a placeholder
        user_id = "current_user"  # Extract from token
        
        repos = RepositoryFactory(db)
        user = repos.users.get_or_create_user(user_id)
        
        return UserInfo(
            user_id=user.user_id,
            is_logged_in=user.is_logged_in,
            login_time=user.login_time,
            created_at=user.created_at
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )


@router.get("/validate")
async def validate_session(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db_session)
):
    """Validate current session token"""
    try:
        # Validate token logic here
        return {"valid": True, "message": "Session is valid"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid session token"
        )


# Dependency for protected routes
async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db_session)
) -> str:
    """Dependency to get current user ID from token"""
    try:
        # In production, decode JWT token here
        # For now, return a placeholder
        return "current_user"
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
