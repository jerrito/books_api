from sqlmodel.ext.asyncio.session import AsyncSession
from .models import UserModel
from .schemas import CreateUserModel
from sqlmodel import select
from .utils import generate_password_hash
from sqlalchemy.orm import selectinload

class UserService:
    async def get_user_by_email(self,email:str, session: AsyncSession) -> UserModel:
        statement = select(UserModel).where(UserModel.email == email).options(selectinload(UserModel.books))
        result = await session.execute(statement)
        user= result.scalar_one_or_none()
        return user

    async def check_user_exist(self,email:str,session:AsyncSession):
        user = await self.get_user_by_email(email,session)
        return True if user is not None else False  

    async def create_user(self, user: CreateUserModel, session: AsyncSession):
        user_data = user.model_dump()
        
        # Hash the password and remove the plain password from user_data
        hashed_password = generate_password_hash(user_data.pop('password'))
        
        # Create new user with the remaining data
        new_user = UserModel(**user_data)
        new_user.password_hash = hashed_password
        
        session.add(new_user)
        await session.commit()
        # await session.refresh(new_user)  # Refresh to get auto-generated fields
        return await self.get_user_by_email(new_user.email, session)
 