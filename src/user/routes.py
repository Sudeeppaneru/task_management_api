from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.models import User
from src.auth.dependencies import get_current_active_user
from src.user.dtos import UserResponse, UserUpdate
from src.user.controller import get_user_profile, update_user_profile

user_routes = APIRouter(prefix="/users", tags=["Users"])


@user_routes.get("/me", response_model=UserResponse)
def get_my_profile(current_user: User = Depends(get_current_active_user)):
    return get_user_profile(current_user)


@user_routes.patch("/me", response_model=UserResponse)
def update_my_profile(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return update_user_profile(db, current_user, update_data)
