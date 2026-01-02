from fastapi import APIRouter,Depends,HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.reviews.models import ReviewModel
from src.reviews.schemas import ReviewResponseModel,CreateReviewModel
from src.reviews.service import ReviewService
from  src.auth.dependencies import AccessTokenBearer
from typing import List



reviewsRouter = APIRouter()


review_service = ReviewService()

@reviewsRouter.post("/", response_model=ReviewResponseModel)
async def create_review(review: CreateReviewModel, session: AsyncSession = Depends(get_session),
token_details:dict = Depends(AccessTokenBearer()),):

    return await review_service.create_review(token_details,review, session)


@reviewsRouter.get("/{review_id}",response_model=ReviewModel)
async def get_review_by_id(review_id:str, session: AsyncSession = Depends(get_session)):
    review = await review_service.get_review_by_id(review_id,session)
    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )

    else:
        return review


@reviewsRouter.get("/user/{user_id}",response_model=List[ReviewModel])
async def get_user_reviews(user_id:str,session: AsyncSession = Depends(get_session)):
    reviews = await review_service.get_reviews_by_user_id(user_id,session)
    if reviews is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return reviews  


@reviewsRouter.get("/book/{book_id}",response_model=List[ReviewModel])
async def get_user_reviews(book_id:str,session: AsyncSession = Depends(get_session)):
    reviews = await review_service.get_reviews_by_book_id(book_id,session)
    if reviews is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    else:
        return reviews    