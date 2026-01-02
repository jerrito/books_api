from uuid import UUID, uuid4
from sqlmodel import  SQLModel, table, Field,Column,Relationship
from datetime import date, datetime
import sqlalchemy.dialects.postgresql as pg
from typing import Optional, TYPE_CHECKING
if TYPE_CHECKING:
    from src.book_service.models import BookModel
    from src.auth.models import UserModel

class ReviewModel(SQLModel,table=True):
    __tablename__ = "reviews"
    uid: UUID = Field(
        sa_column= Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default= uuid4
        )
    )
    review_text: str = Field(max_length=255)
    rating: int = Field(
        max_length=5,
        
    )
    book_uid: UUID = Field(
        foreign_key="books.uid",
        nullable=False
    )
    user_uid: UUID = Field(
        foreign_key="users.uuid",
        nullable=False
    )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now,),)
    updated_at: datetime = Field(sa_column= Column(pg.TIMESTAMP, default= datetime.now))
    book: "BookModel" = Relationship(back_populates="reviews")
    user: "UserModel" = Relationship(back_populates="reviews")


def __repr__(self) -> str: 
    return f"<Review for {self.user_uid} on book {self.book_uid} with review {self.review_text}>"   