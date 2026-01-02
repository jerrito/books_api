from pydantic import BaseModel
from datetime import datetime
class ReviewResponseModel(BaseModel):
    review_text: str
    rating: int
    created_at: datetime
    updated_at: datetime
    book_uid: str
    user_uid: str


class CreateReviewModel(BaseModel):
    review_text: str
    rating: int
    book_uid: str
    user_uid: str