from fastapi.security import HTTPBearer
from fastapi import Request,HTTPException,status, Depends
from fastapi.security.http import HTTPAuthorizationCredentials
from src.auth.utils import decode_token
from src.db.redis import get_jti_in_blocklist
from sqlmodel.ext.asyncio.session import AsyncSession
from ..db.main import get_session
from src.auth.service import UserService
from typing import List, Any
from src.auth.models import UserModel


user_service = UserService()
class TokenBearer(HTTPBearer):
    def __init__(self,auto_error= True):
        super().__init__(auto_error= auto_error)

    async def __call__(self,request:  Request) -> HTTPAuthorizationCredentials | None:
        credit = await super().__call__(request)
        token = credit.credentials
        # try:
        token_data= await decode_token(token)
        if not await self.is_token_valid(token):
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid or expired token")


        if (await get_jti_in_blocklist(token_data['jti'])):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={
                        "error": "This token is invalid or has been revoked",
                        "resolution": "Please get new token"
                    }
                )



        self.verify_token_data(token_data)
        return token_data   
        # except Exception as e:
        #      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid or expired token")  

    async def is_token_valid(self, token: str) -> bool:
        token = await decode_token(token)
        return True if token is not None else False    

    def verify_token_data(self,token_data: dict):
        
        raise NotImplementedError("Please implement this method in child class")
        


class AccessTokenBearer(TokenBearer):
    def verify_token_data(self,token_data: dict)-> None:
        if(token_data and token_data['refresh']):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Please provide an access token")
        


class RefreshTokenBearer(TokenBearer):
    def verify_token_data (self,token_data: dict) -> None:
        if(token_data and not token_data['refresh']):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Please provide a refresh token")
        


async def get_current_user(token_details:dict = Depends(AccessTokenBearer()),session: AsyncSession = Depends(get_session)):
    current_user =  token_details['user']
    email = current_user['email']
    user = await user_service.get_user_by_email(email,session)
    return user
     



class RoleCheck():
    def __init__(self,allowed_roles:List[str]):
        self.allowed_roles= allowed_roles 


    def __call__(self, user:UserModel= Depends(get_current_user)) -> Any:
        if(user.role not in self.allowed_roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You are not authorized to access this resource")
        return True    