from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Optional
from config.database import get_db
from models.todo_model import User
from jose import jwt, JWTError
import os

from dotenv import load_dotenv

load_dotenv()
onAuthSchema = OAuth2PasswordBearer(tokenUrl="token")
pwd_context= CryptContext(schemes=["bcrypt"], default="bcrypt")
# def get_current_user(token: str, db: Session = Depends(get_db)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
#         username: str = payload.get("user_name")
#         userid= payload.get("user_id")
        
#         if username is None:
#             raise credentials_exception
#         if userid is None:
#             raise credentials_exception
#     except JWTError:
#         raise credentials_exception
#     user = get_user(db, username)
#     if user is None:
#         raise credentials_exception
#     return user
# def get_user(db: Session, username: str):
#     return db.query(User).filter(User.username == username).first()


def verify_token(token:str = Depends(onAuthSchema)):
    try:
        # decode the token 
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        username: str = payload.get("user_name")
        userid = payload.get("user_id")
        if username is None or userid is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"username": username, "userid": userid}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    print("in the hash block ")
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    try:
        print("in the jwt block ")
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode,os.getenv("SECRET_KEY") , algorithm=os.getenv("ALGORITHM"))
    except Exception as e:
        print(e)
        print("An exception is accure")
        return None
    
def decode_access_token(token:str):
    try:
        payload = jwt.decode(token,os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        return payload
    except JWTError as e:
        print(e)
        return None
