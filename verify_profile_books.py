
import asyncio
import sys
import os
from uuid import uuid4
from datetime import date

# Add project root to sys.path
sys.path.append(os.getcwd())

from src.db.main import async_session
from src.auth.service import UserService
from src.auth.schemas import CreateUserModel, UserResponse
from src.book_service.models import BookModel
from src.auth.models import UserModel

async def verify_fix():
    print("Verifying MissingGreenlet fix...")
    
    # Generate unique email to avoid conflicts
    unique_id = str(uuid4())[:8]
    email = f"test_{unique_id}@example.com"
    username = f"user_{unique_id}"
    
    user_service = UserService()
    
    async with async_session() as session:
        try:
            # 1. Create a user
            print(f"Creating user {email}...")
            create_user_model = CreateUserModel(
                username=username,
                email=email,
                first_name="Test",
                last_name="User",
                password="password123"
            )
            user = await user_service.create_user(create_user_model, session)
            user_uid = user.uuid
            
            # 2. Create a book associated with the user manually
            print("Creating a book for the user...")
            book = BookModel(
                title="Test Book",
                author="Test Author",
                publisher="Test Publisher",
                published_date=date.today(),
                language="English",
                pages=100,
                isbn=f"ISBN-{unique_id}",
                price=19.99,
                available=True,
                user_uid=user_uid # Assuming this FK exists, checking models next if it fails
            )
            # Check UserModel relationship to be sure
            # user.books.append(book) - better to add book with FK
            # But BookModel definition in previous turns (Step 16) didn't show user_uid FK explicitly?
            # Let's check BookModel in a sec if this fails.
            # Actually, let's just add it to the user object if possible, or session.add(book)
            
            # Re-reading BookModel from Step 16:
            # class BookModel(SQLModel,table=True): ...
            # It didn't show user relationship in the snippet in Step 16.
            # But UserModel has `books: list[BookModel] = Relationship(back_populates="user")` (Step 126).
            # So BookModel MUST have a `user` relationship or `user_uid` FK.
            # If I can't easily add a book, the empty list should still be eager loaded.
            # The error presumably happens even if list is empty if it's accessed and not loaded?
            # Actually, empty list might not trigger it if it defaults to [] in python but SA might still try to load.
            # Let's try to fetch the user.
            
            # 3. Fetch the user using the service method (which should now have selectinload)
            print("Fetching user by email...")
             # We need a new session or expire the current one to force reload? 
            # create_user commits and refreshes.
            
        except Exception as e:
            print(f"Setup failed: {e}")
            return

    # Use a NEW session to ensure we are testing the query loading
    async with async_session() as session:
        try:
             fetched_user = await user_service.get_user_by_email(email, session)
             
             if not fetched_user:
                 print("Error: User not found!")
                 sys.exit(1)
                 
             print("User fetched. Attempting to access books...")
             # This is the critical part that would raise MissingGreenlet if not eager loaded
             books = fetched_user.books
             print(f"Success: Accessed books: {books}")
             
             # Also try validating with UserResponse schema as the route does
             print("Validating with UserResponse schema...")
             UserResponse.model_validate(fetched_user)
             print("Success: UserResponse validation passed.")
             
        except Exception as e:
            print(f"Failure: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == "__main__":
    asyncio.run(verify_fix())
