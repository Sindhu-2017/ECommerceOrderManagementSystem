from datetime import datetime,timedelta,timezone
import hashlib
import jwt
from pwdlib import PasswordHash
import uuid


from app.core.config import get_settings

password_hash = PasswordHash.recommended()
settings= get_settings()

def hash_password(password:str)->str:
    return password_hash.hash(password)

def verify_password(plain_password:str,hashed_password:str)->bool:
    return password_hash.verify(plain_password,hashed_password)

def create_token(user_id:int,role:str,token_type:str,expires_delta:timedelta)->tuple[str,str,datetime]:
    now=datetime.now(timezone.utc)
    expires_at = now+expires_delta
    jti=str(uuid.uuid4())
    payload :dict={
        "sub":str(user_id),
        "role":role,
        "type":token_type,
        "jti":jti,
        "iat":now,
        "exp":expires_at
    }
    token =jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return token,expires_at

def create_access_token(user_id:int,role:str) ->str:
    token,_=create_token(
        user_id=user_id,
        role=role,
        token_type="access",
        expires_delta=timedelta(
            settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )        
    )
    return token

def create_refresh_token(user_id:int,role:str)->tuple:
    return create_token(
        user_id=user_id,
        role=role,
        token_type="refresh",
        expires_delta=timedelta(
            settings.REFRESH_TOKEN_EXPIRE_DAYS
        ),
        options={
            "require":[
                "sub","exp","iat","jti","type"
            ],
        }   
    )

def decode_token(token:str)->dict:
    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

def hash_refresh_token(token:str)->str:
    return hashlib.sha256(
        token.encode("utf-8")
    ).hexdigest()