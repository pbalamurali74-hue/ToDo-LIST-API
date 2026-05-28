import re
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator

EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


class UserRegister(BaseModel):
    name: str = Field(..., min_length=2, description="Name must be at least 2 characters")
    email: str = Field(...)
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if not re.match(EMAIL_REGEX, v):
            raise ValueError("Invalid email address format")
        return v.lower()


class UserLogin(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        return v.lower()


class TokenResponse(BaseModel):
    token: str
    refreshToken: str


class RefreshRequest(BaseModel):
    refreshToken: str


class TokenRefreshResponse(BaseModel):
    token: str


class TodoCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(default="")


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    description: Optional[str] = Field(default=None)
    completed: Optional[bool] = Field(default=None)


class TodoResponse(BaseModel):
    id: str
    title: str
    description: str
    completed: bool

    class Config:
        from_attributes = True


class PaginatedTodoResponse(BaseModel):
    data: List[TodoResponse]
    page: int
    limit: int
    total: int
