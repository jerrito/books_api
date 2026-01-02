from fastapi import Depends,HTTPException,status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.reviews.models import ReviewModel
from src.auth.models import UserModel
from src.auth.service import UserService
from  src.auth.dependencies import AccessTokenBearer
from src.auth.dependencies import get_current_user
from src.book_service.models import BookModel
from src.book_service.service import BookService
from sqlmodel import select


book_service = BookService()
class ReviewService:
    async def create_review(self, token_details:dict,review: ReviewModel, session: AsyncSession ):
        user = await get_current_user(token_details,session=session)

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found")

        book= await book_service.get_book_by_id(session=session,book_id=review.book_uid)
        if book is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found")
        review_data= review.model_dump()
        new_review= ReviewModel(**review_data)
        session.add(new_review)
        await session.commit()
        return new_review

    async def get_review_by_id(self, review_id: str, session: AsyncSession = Depends(get_session)):
        try:
           statement= select(ReviewModel).where(review_id== ReviewModel.uid)
           result= await session.execute(statement)
           return result.scalar_one_or_none()
        except:
            return None   

    async def get_reviews_by_book_id(self, book_id: str, session: AsyncSession = Depends(get_session)):
        try:
            statement= select(ReviewModel).where(book_id== ReviewModel.book_uid)
            result =await session.execute(statement)
            return result.scalars().all()
        except:
            return None    

    async def get_reviews_by_user_id(self, user_id: str, session: AsyncSession = Depends(get_session)):
        try:
            statement= select(ReviewModel).where(user_id== ReviewModel.user_uid)
            result =await session.execute(statement)
            return result.scalars().all()
        except:
            return None

    async def update_review(self, review_id: int, review: ReviewModel, session: AsyncSession = Depends(get_session)):
        pass

    async def delete_review(self, review_id: int, session: AsyncSession = Depends(get_session)):
        pass
