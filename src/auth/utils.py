import bcrypt
from datetime import timedelta, datetime, timezone
import jwt 
from src.config import SettingsConfig
from uuid import uuid4
import logging

Access_Token_Expiry= 3600

def generate_password_hash(password: str) -> str:
    """Hash a password using bcrypt.
    
    Args:
        password: The plain text password to hash
        
    Returns:
        The hashed password as a string
    """
    # Convert password to bytes and hash it
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    # Return as string for storage
    return hashed.decode('utf-8')


def verify_password(password: str, hash_password: str) -> bool:
    """Verify a password against a hash.
    
    Args:
        password: The plain text password to verify
        hash_password: The hashed password to check against
        
    Returns:
        True if password matches, False otherwise
    """
    password_bytes = password.encode('utf-8')
    hash_bytes = hash_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hash_bytes)
     

async def create_access_token(user_data:dict,expiry:timedelta = None,refresh: bool =False):
    payload= {}
    payload['user']= user_data
    expire = datetime.now(timezone.utc) + (expiry if expiry is not None else timedelta(seconds=Access_Token_Expiry))
    
    payload['exp'] = int(expire.timestamp()) 
    payload['jti'] = str(uuid4())
    payload['refresh']= refresh
    payload['role']= user_data['role']

    token = jwt.encode(
        payload=payload,
        key= SettingsConfig.JWT_SECRETE_KEY,
        algorithm=SettingsConfig.JWT_ALGORITHM 
    )
    return token 


async def decode_token(token:str)-> dict:
    try:
        token_data= jwt.decode(
        jwt=token,
        algorithms=SettingsConfig.JWT_ALGORITHM,
        key=SettingsConfig.JWT_SECRETE_KEY
        )
        if(token_data != None):

          return token_data
        else:
          return None
    except jwt.exceptions.ExpiredSignatureError as e:
        logging.log(msg=e,level=logging.ERROR) 
        return None   
    except jwt.exceptions.InvalidTokenError as e:
        logging.log(msg=e,level=logging.ERROR) 
        return None   
    except jwt.PyJWTError as e:
        logging.log(msg=e,level=logging.ERROR) 
        return None    