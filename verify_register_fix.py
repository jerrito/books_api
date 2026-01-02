
import asyncio
import sys
import os
from uuid import uuid4

# Add project root to sys.path
sys.path.append(os.getcwd())

from src.db.main import async_session
from src.auth.service import UserService
from src.auth.schemas import CreateUserModel, UserResponse

async def verify_register_fix():
    print("Verifying Register Endpoint fix...")
    
    # Generate unique email to avoid conflicts
    unique_id = str(uuid4())[:8]
    email = f"test_reg_{unique_id}@example.com"
    username = f"user_{unique_id}"
    
    user_service = UserService()
    
    async with async_session() as session:
        try:
            # 1. Register a new user
            print(f"Registering user {email}...")
            create_user_model = CreateUserModel(
                username=username,
                email=email,
                first_name="Test",
                last_name="User",
                password="password123"
            )
            
            # This calling create_user should now return a user with books loaded
            new_user = await user_service.create_user(create_user_model, session)
            
            print("User registered. Attempting to access books...")
            
            # 2. Access books to verify fix
            # This is where it would crash if the fix didn't work
            books = new_user.books
            print(f"Success: Accessed books: {books}")
            
            # 3. Validate against UserResponse
            print("Validating with UserResponse schema...")
            UserResponse.model_validate(new_user)
            print("Success: UserResponse validation passed.")
             
        except Exception as e:
            print(f"Failure: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == "__main__":
    asyncio.run(verify_register_fix())
