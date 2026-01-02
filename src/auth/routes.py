from fastapi import APIRouter,Depends,HTTPException,status
from .schemas import CreateUserModel, UserResponse
from .service import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from ..db.main import get_session
from src.auth.utils import verify_password, create_access_token
from src.auth.schemas import LoginModel
from datetime import timedelta
from fastapi.responses import JSONResponse 
import logging
from src.auth.dependencies import AccessTokenBearer
import time,datetime
from src.db.redis import add_jti_to_blocklist
from src.auth.dependencies import get_current_user
from src.auth.dependencies import RoleCheck



authRouter= APIRouter()
user_service = UserService()

role_check= RoleCheck(allowed_roles=["admin","user"])
@authRouter.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: CreateUserModel, session: AsyncSession = Depends(get_session)):
    user_exist=await user_service.check_user_exist(user.email,session)
    if user_exist :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
        detail="User email already exist")
    else:
        new_user= await user_service.create_user(user,session) 
        return new_user   


@authRouter.get("/user", response_model=UserResponse,dependencies=[Depends(role_check)])
async def get_user(email: str, session: AsyncSession = Depends(get_session)):
    user = await user_service.get_user_by_email(email, session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@authRouter.post("/login",response_model=UserResponse,status_code=status.HTTP_200_OK)
async def login(user_data:LoginModel,session: AsyncSession = Depends(get_session)):
    
    email= user_data.email
    password= user_data.password
    user= await user_service.get_user_by_email(email,session)
   
    print(user.email)
        
    if(user is not None):
        isPasswordValid= verify_password(password, user.password_hash)
        print(isPasswordValid)
        if isPasswordValid :
            access_token=await  create_access_token(
            user_data={
                'email': user.email,
                        'user_uid':str(user.uuid),
                        "role":user.role
                    }
                )
            refresh_token= await create_access_token(
                    user_data={
                         'email': user.email,
                        'user_uid':str(user.uuid),
                        "role":user.role
                    },
                    refresh=True,
                    expiry= timedelta(days=2 )
                )
            return JSONResponse(
                    content={
                        "message":"Login successful",
                        "access_token":access_token,
                        "refresh_token": refresh_token,
                        "user":user.model_dump(exclude={"password_hash","created_at","updated_at","uuid"}),
                        "uuid": str(user.uuid)
                    } 
            )
        else: 
                raise HTTPException(status_code=409,detail="Invalid password")


@authRouter.get("/refresh_token",dependencies=[Depends(role_check)])
async def get_new_access_token(data:dict = Depends(AccessTokenBearer())):
    expiry_timestamp= data['exp']
    if(expiry_timestamp is None):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail={
                        "error": "Token expiry is missing",
                        "resolution": "Please get new token"
                    })

    elif(datetime.datetime.fromtimestamp(expiry_timestamp) < datetime.datetime.now()):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail={
                        "error": "This token is invalid or has been revoked",
                        "resolution": "Please get new token"
                    })    
    else:
        access_token= await create_access_token(
            user_data=data["user"]
        )
        return JSONResponse(
            content={ 
                "access_token":access_token,
                "token_type":"Bearer"
            },
        )



@authRouter.post("/logout",dependencies=[Depends(role_check)])
async def logout(data:dict = Depends(AccessTokenBearer())):
    await add_jti_to_blocklist(data['jti'])
    return JSONResponse(
        content={
            "message":"Logout successful"
        }
    )


@authRouter.get("/me",dependencies=[Depends(role_check)], response_model=UserResponse)
async def get_current_user(user: UserResponse = Depends(get_current_user)):
    return user
