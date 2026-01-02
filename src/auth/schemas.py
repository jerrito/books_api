from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from src.book_service.schema import BookModel
from src.reviews.models import ReviewModel

class CreateUserModel(BaseModel):
    """Schema for user registration request."""
    username: str = Field(max_length=8)
    email: str = Field(max_length=255)
    first_name: str
    last_name: str
    password: str = Field(min_length=8, max_length=255)


class UserResponse(BaseModel):
    """Schema for user response (excludes password_hash)."""
    model_config = ConfigDict(from_attributes=True)
    
    uuid: UUID
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool 
    created_at: datetime  
    updated_at: datetime
    books: list[BookModel] = []
    reviews: list[ReviewModel] = []


class LoginModel(BaseModel):
    email: str = Field(max_length=255)
    password: str = Field(min_length=8, max_length=255)
