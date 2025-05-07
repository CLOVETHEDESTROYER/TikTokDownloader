from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from ...models.user import Token, User
from ...core.security import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_admin_user
)
from ...core.config import settings

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Get an access token for authentication.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Get information about the current user.
    """
    return current_user


@router.get("/admin-check")
async def admin_protected_route(admin_user: User = Depends(get_admin_user)):
    """
    This route is protected and can only be accessed by admin users.
    """
    return {
        "message": "You have admin access",
        "user": admin_user.email
    }
