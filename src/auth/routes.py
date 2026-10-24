from fastapi import APIRouter, Depends, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.utils.db import get_db
from src.auth.dtos import UserRegister, LoginRequest, Token
from src.auth.service import register_user, authenticate_user
from src.user.dtos import UserResponse

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    user = register_user(db, user_data)
    return user


@auth_router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # OAuth2PasswordRequestForm uses username field for username or email
    login_data = LoginRequest(email=form_data.username if "@" in form_data.username else None,
                              username=form_data.username if "@" not in form_data.username else None,
                              password=form_data.password)
    token = authenticate_user(db, login_data)
    return {"access_token": token, "token_type": "bearer"}


@auth_router.post("/login/json", response_model=Token)
def login_json(login_data: LoginRequest, db: Session = Depends(get_db)):
    token = authenticate_user(db, login_data)
    return {"access_token": token, "token_type": "bearer"}
