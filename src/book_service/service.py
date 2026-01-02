from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select
from uuid import UUID

from src.book_service.models import BookModel
from src.book_service.schema import BookCreateModel, UpdateBookModel

class BookService:
    
    async def get_all_books(self, session: AsyncSession):
        statement = select(BookModel).order_by(BookModel.created_at.desc())
        result = await session.execute(statement)
        return result.scalars().all()
    
    async def get_book_by_id(self, session: AsyncSession, book_id: str):
        try:
           statement = select(BookModel).where(BookModel.uid == book_id)
           result = await session.execute(statement)
           book = result.scalar_one_or_none()
           return book
        except Exception as e:
            print(f"Error getting book by id: {e}")
            return None
    async def get_book_by_isbn(self, session: AsyncSession, book_isbn: str):
        try:
            statement = select(BookModel).where(BookModel.isbn == book_isbn)
            print(f"statement: {statement}")
            
            result = await session.execute(statement)
            book = result.scalar_one_or_none()
            if(book is not None):
                print(f"Book exist: {book}")
                return True
            else: 
                print("false")
                return False    
        except Exception as e:
            print(f"Error getting book by isbn: {e}")
            return None    
    
    async def create_book(self, session: AsyncSession, user_uid: str,book: BookCreateModel):
        checkBookExist= await self.get_book_by_isbn(session=session,book_isbn=book.isbn)
        print(f"checkBookExist: {checkBookExist}")
        if checkBookExist == False:
             book_data = book.model_dump()
             new_book = BookModel(**book_data)
             new_book.user_uid= user_uid
             session.add(new_book)
             await session.commit()
             await session.refresh(new_book)
             return new_book
        else:
            return None     
    
    async def update_book(self, session: AsyncSession, book_id: str, book: UpdateBookModel):
        update_book = await self.get_book_by_id(session, book_id)
        if update_book is not None:
            update_book_dict = book.model_dump(exclude_unset=True)
            for key, value in update_book_dict.items():
                setattr(update_book, key, value)
            await session.commit()
            await session.refresh(update_book)
            return update_book
        else:
            return None

    async def delete_book(self, session: AsyncSession, book_id: str):
        delete_book = await self.get_book_by_id(session, book_id)
        if delete_book is not None:
            await session.delete(delete_book)
            await session.commit()
            return delete_book
        else:
            return None    

    async def get_user_book_submissions(self,session:AsyncSession,user_uid:str):
        statement = select(BookModel).where(BookModel.user_uid == user_uid).order_by(BookModel.created_at.desc())
        result = await session.execute(statement)
        books = result.scalars().all()  
        return books      