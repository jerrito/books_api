
import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())

from src.auth.utils import create_access_token, decode_token
from datetime import timedelta
import logging

# Configure logging to capture output
logging.basicConfig(level=logging.INFO)

def test_jwt_serialization():
    print("Testing JWT serialization...")
    user_data = {"email": "test@example.com", "user_uid": "12345"}
    
    try:
        # Attempt to create a token
        token = create_access_token(user_data=user_data, expiry=timedelta(minutes=15))
        print("Success: Token created successfully.")
        print(f"Token: {token}")
        
        # Verify decoding
        decoded = decode_token(token)
        if decoded and 'exp' in decoded:
             print("Success: Token decoded successfully and contains 'exp' claim.")
             print(f"Decoded payload: {decoded}")
        else:
             print("Failure: Token decoding failed or missing 'exp' claim.")
             sys.exit(1)

    except Exception as e:
        print(f"Failure: An error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_jwt_serialization()
