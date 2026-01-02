from fastapi import FastAPI,Depends
from src.book_service.routes import book_router
from contextlib import asynccontextmanager
from src.db.main import init_db
from .auth.routes import authRouter
from .reviews.routes import reviewsRouter
from .auth.dependencies import RoleCheck
role_check= RoleCheck(allowed_roles=["admin","user"])

version = "v1"
api = '/api/'

@asynccontextmanager
async def life_span(app:FastAPI):
    print(f'Server has started')
    await init_db()
    yield
    print(f'Server has been stopped')

app = FastAPI(
    version=version,
    title = "Bookly",
    description= "This is a fastapi bookly api",
    # lifespan=life_span
)

@app.get("/health")
def get_health():
    return {"message": "Healthy Api running"}

app.include_router(book_router,prefix=f"{api}{version}/books", tags= ["books"],dependencies=[Depends(role_check)])
app.include_router(authRouter,prefix=f"{api}{version}/auth", tags=["auth"])
app.include_router(reviewsRouter,prefix=f"{api}{version}/reviews", tags=["reviews"],dependencies=[Depends(role_check)]) 