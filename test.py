from fastapi import FastAPI,Header
from typing import Optional
from pydantic import BaseModel
app=FastAPI()


@app.get("/")
async def getRoot():
    return {"message":"Welcome to fastapi tutorials"}


# using path providers
@app.get("/name/{name}")
async def get_name(name:str) -> dict:
    return {"name":f"User name is {name}"}

# using query params
@app.get("/username")
async def get_username(name:str)-> dict:
    return {"name": f"Username is {name}"}



#using both path and query params
@app.get("/greet/{name}")
def  greet(name:str,age:Optional[int]=30):
    return {"data":f"Hello I am {name} \nI am {age} years old"}



# create book model
class CreateBookModel(BaseModel):
    title: str
    author: str



# create book
@app.post("/create_book")
async def create_book(create_book_model:CreateBookModel):
    return {
        "title":create_book_model.title,
        "author":create_book_model.author
    }


# get hearders
@app.get("/headers",status_code=201)
async def get_headers(
    accept:str =Header(None),
    content_type:str = Header(None),
    user_agent:str = Header(None),
    host:str = Header(None)
):
    request_headers={}
    request_headers["Accept"]= accept
    request_headers["Content_Type"] = content_type
    request_headers["User_Agent"] = user_agent
    request_headers["Host"] = host 
 
    return request_headers