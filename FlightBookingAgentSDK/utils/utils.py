from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer,APIKeyHeader
from datetime import datetime, timedelta
from passlib.context import CryptContext
from typing import Optional
from config.dataBase import db
from fastapi_mail import FastMail, MessageSchema
from pydantic import EmailStr
from config.email_configuration import conf
import random
# from models.todo_model import User
from jose import jwt, JWTError
import os

from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")
onAuthSchema = OAuth2PasswordBearer(tokenUrl="token")
api_key_header = APIKeyHeader(name="api_key", auto_error=False)
pwd_context= CryptContext(schemes=["bcrypt"], default="bcrypt")

def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != os.getenv("API_KEY"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return api_key
    
def verify_token(token:str = Depends(onAuthSchema)):
    try:
        # decode the token 
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        user_from_token = {
            "user_id": payload.get("user_id"),
            "user_name": payload.get("user_name"),
            "user_email":payload.get("user_email")
        }
        print("the token from the user ", user_from_token,payload)
        if user_from_token is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {
            "user_id": user_from_token.get("user_id"),
            "user_name": user_from_token.get("user_name"),
            "user_email": user_from_token.get("user_email")
        }
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

# create a random 6 digit number
def generate_otp():
    
    return random.randint(100000, 999999)
async def send_otp_email(email: EmailStr, otp_code):
    # otp_code = generate_otp()

    message = MessageSchema(
        subject="Your OTP Code",
        recipients=[email],
        body=f"Your OTP code is: {otp_code}",
        subtype="plain"
    )

    fm = FastMail(conf)
    await fm.send_message(message)

    return {
        "data": {
            "otp_code": otp_code
        },
        "message": "OTP sent successfully",
        "status": "success"
    }