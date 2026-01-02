
import sys
import os
import asyncio
from unittest.mock import MagicMock

# Add the project root to sys.path
sys.path.append(os.getcwd())

from src.auth.utils import create_access_token
from src.auth.dependencies import AccessTokenBearer
from fastapi import Request
from datetime import timedelta

async def test_auth_dependencies():
    print("Testing Auth Dependencies...")
    
    # 1. Create a valid token
    user_data = {"email": "test@example.com", "user_uid": "12345"}
    token = await create_access_token(user_data=user_data, expiry=timedelta(minutes=10))
    print(f"Created Token: {token}")

    # 2. Mock Request object
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Instantiate AccessTokenBearer
    access_token_bearer = AccessTokenBearer()
    
    try:
        # 4. Call the bearer (mimics dependency injection)
        # Note: We need to see if we can call it directly. 
        # TokenBearer inherits from HTTPBearer. HTTPBearer.__call__ expects a Request.
        
        # We need to simulate the super().__call__ behavior if we can't easily mock it entirely.
        # However, since we are testing logic *inside* our class, let's try calling it.
        # But wait, HTTPBearer implementation in FastAPI reads from headers.
        
        token_data = await access_token_bearer(mock_request)
        print("Success: AccessTokenBearer returned token data without error.")
        print(f"Token Data: {token_data}")
        
    except NotImplementedError:
        print("Failure: NotImplementedError was raised!")
        sys.exit(1)
    except Exception as e:
        print(f"Failure: An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(test_auth_dependencies())
