from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
from src.models import User
from src.user.dtos import UserUpdate


def get_user_profile(user: User) -> User:
    return user


def update_user_profile(db: Session, user: User, update_data: UserUpdate) -> User:
    update_dict = update_data.model_dump(exclude_unset=True)

    # Check uniqueness if username or email is being updated
    if "username" in update_dict and update_dict["username"] != user.username:
        existing = db.query(User).filter(User.username == update_dict["username"]).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username already taken"
            )

    if "email" in update_dict and update_dict["email"] != user.email:
        existing = db.query(User).filter(User.email == update_dict["email"]).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already taken"
            )

    for field, value in update_dict.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user
