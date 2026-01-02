from fastapi import FastAPI, APIRouter, HTTPException, status, Depends
from src.book_service.schema import BookModel, UpdateBookModel, BookCreateModel
from src.book_service.book_data import books 
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from src.book_service.service import BookService
from src.auth.dependencies import AccessTokenBearer
book_router = APIRouter()

book_service =  BookService()

access_token_bearer = AccessTokenBearer()

# get all books
@book_router.get("/",response_model=List[BookModel])
async def get_all_books(session:AsyncSession = Depends(get_session),token_details= Depends(  access_token_bearer)):
    books = await book_service.get_all_books(session)
    print(token_details)
    return  books


# get book by id
@book_router.get("/{id}", response_model=BookModel) 
async def get_book_by_id(id: UUID, session: AsyncSession = Depends(get_session),
     token_details: dict= Depends(access_token_bearer)
    ):
    book = await book_service.get_book_by_id(session=session, book_id=str(id))
    if book:
        return book
    else:
        raise HTTPException(status_code=404, detail="Book not found")    






# create book 
@book_router.post("/", status_code=status.HTTP_201_CREATED, response_model=BookModel)
async def create_book(book: BookCreateModel, session: AsyncSession = Depends(get_session),
        token_details : dict= Depends(access_token_bearer)
    ):
    user_uid = token_details.get("user")["user_uid"]
    
    new_book = await book_service.create_book(session, user_uid=user_uid, book=book)

    if new_book is not None:
        return new_book
    raise HTTPException(status_code=400, detail="Book already exist with that isbn")    

# update book by id
@book_router.patch("/{id}", response_model=BookModel)
async def update_book(id: UUID, book_update_data: UpdateBookModel, session: AsyncSession = Depends(get_session),user_details: dict= Depends(access_token_bearer)):
    book = await book_service.update_book(session, book_id=str(id), book=book_update_data)
    if book is not None:
        return book
    else:
        raise HTTPException(status_code=404, detail="Book not found")  
       



# delete book by id
@book_router.delete("/{id}")
async def delete_book(id: UUID, session: AsyncSession = Depends(get_session),token_details : dict= Depends(access_token_bearer)):
    book = await book_service.delete_book(session=session, book_id=str(id))
    if book is not None:
        return {"message":"Successfully deleted","data":book}
    else:
        raise HTTPException(status_code=404, detail="Book not found")      


# get user book submissions
@book_router.get("/user/{user_uid}",response_model=List[BookModel])
async def get_user_book_submissions(user_uid: str, session: AsyncSession = Depends(get_session)):   
    books = await book_service.get_user_book_submissions(session, user_uid=user_uid)
    if books is not None:

      return books
    else:
        raise HTTPException(status_code=404, detail="No book found")  












# # get all books
# @book_router.get("/",response_model=List[BookModel])
# async def get_all_books(session:AsyncSession = Depends(get_session)):
#     return  books


# # get book by id
# @book_router.get("/{id}") 
# async def get_book_by_id(id:int)-> dict:
#     try:
#         # book= books[id-1]
#         # return {
#         # "data":book
#         # } 
#         for book in books:
#             print(book['id'])
#             if book['id'] == id:
#                 return {
#                     "data": book
#                 }
#         raise HTTPException(status_code=404,detail="Book not found")        
#     except:
#         error= HTTPException(status_code=404,detail="Book not found")   
#         raise error






# # create book 
# @book_router.post("/",status_code=status.HTTP_201_CREATED)
# async def create_book(book:BookModel):
#     print("ss")
   
#     logging.debug(f"jdjdjj")
#     print(books[0]["id"])
#     # check books id is already exist
#     if book.id in [book["id"] for book in books]:
#         raise HTTPException(status_code=401,)
#     else:
#         new_book = book.model_dump()
#         books.book_routerend(new_book)
#         return {
#             "status": "true",
#             "book":new_book
#                  }
#     # except Exception as e: 
#     #     return {"error":HTTPException(status_code=401,detail=e) } 

# # update book by id
# @book_router.patch("/{id}")
# async def update_book(id:int,book_update_data:UpdateBookModel) -> dict:
 
#     book=await get_book_by_id(id)
#     print(book["data"])
#     if book["data"]["id"]== id:
#         book["data"]["title"]=book_update_data.title
#         book["data"]["author"]= book_update_data.author
#         book["data"]["publisher"]= book_update_data.publisher
#         book["data"]["price"]= book_update_data.price
#         book["data"]["language"]= book_update_data.language
#         book["data"]["available"]= book_update_data.available
#         return {"message":"Update success","data":book}
#     else:
#         raise HTTPException(status_code=404,detail="Book not found")  
       



# # delete book by id
# @book_router.delete("/{id}")
# async def delete_book(id:int)-> dict:
#     try:
#         book=await get_book_by_id(id)
#         books.remove(book["data"])
#         return {"message":"Delete success"}  
#     except:
#         raise HTTPException(status_code=404)    