from datetime import datetime, date
from uuid import UUID
from pydantic import BaseModel

class BookModel(BaseModel):
    uid: UUID 
    title: str
    author: str
    publisher: str
    published_date: date
    language: str
    pages: int
    isbn: str
    price: float
    available: bool
    created_at: datetime
    updated_at: datetime

class BookCreateModel(BaseModel):    
    title: str
    author: str
    publisher: str 
    published_date: date
    language: str
    pages: int
    isbn: str
    price: float 
    available: bool

class UpdateBookModel(BaseModel):
    title: str
    author: str
    publisher: str
    language: str
    isbn: str
    price: float
    available: bool
