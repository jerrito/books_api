from uuid import UUID, uuid4
import uuid
from sqlmodel import DateTime, SQLModel, table, Field,Column,Relationship
from datetime import date, datetime
import sqlalchemy.dialects.postgresql as pg
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.auth.models import UserModel
    from src.reviews.models import ReviewModel

class BookModel(SQLModel,table=True):
    __tablename__ = "books"
    uid: UUID = Field(
        sa_column= Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default= uuid4
        )
    )
    title: str
    author: str
    publisher: str
    published_date: date
    language: str
    user_uid:Optional[UUID] = Field(
        default= None,
        foreign_key="users.uuid",
        nullable= True
    )
    pages: int
    isbn: str
    price: float
    available: bool
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now,),)
    updated_at: datetime = Field(sa_column= Column(pg.TIMESTAMP, default= datetime.now))
    user: Optional["UserModel"] = Relationship(back_populates="books",
    sa_relationship_kwargs={
        "lazy": "selectin",
    }   )  
    reviews: list["ReviewModel"] = Relationship(back_populates="book",sa_relationship_kwargs={"lazy": "selectin"})

    def __repr__(self) -> str: 
        return f"<Book {self.title}>"