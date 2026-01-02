from sqlmodel import SQLModel,Field, Column,Relationship
from uuid import UUID,uuid4
from datetime import date, datetime
import sqlalchemy.dialects.postgresql as pg
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.reviews.models import ReviewModel
    from src.book_service.models import BookModel

class UserModel(SQLModel,table= True):
    __tablename__ =  'users'
    uuid: UUID=  Field(
    sa_column= Column(
        pg.UUID,
        nullable= False,
        primary_key= True,
        default= uuid4
    )
    )
    username: str
    email: str
    first_name: str
    last_name: str
    password_hash: str= Field(exclude=True)
    is_verified: bool = False
    role: str = Field(
        sa_column= Column(
            pg.VARCHAR,
            nullable= False,
            default= "user",
            server_default= "user"
        )
    )
    created_at: datetime  = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now,),)
    updated_at: datetime  = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now,),)
    books: list["BookModel"] = Relationship(back_populates="user",sa_relationship_kwargs={"lazy": "selectin"})
    reviews: list["ReviewModel"] = Relationship(back_populates="user",sa_relationship_kwargs={"lazy": "selectin"})
 

    # string representation of our model
    def __repr__(self)-> str:
        return f"<User {self.username}> "
