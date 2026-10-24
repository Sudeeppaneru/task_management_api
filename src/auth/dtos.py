from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    phone_no: str | None = Field(default=None, max_length=20)


class LoginRequest(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
