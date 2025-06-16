from fastapi import APIRouter, HTTPException, Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session  
from config.database import get_db
from models.todo_model import Users
from validations.validation import UserCreate,LoginUser

from utils.utils_helper_function import create_access_token,hash_password,verify_password, verify_api_key
user_router = APIRouter()



@user_router.post("/register/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        print("Creating user:", user)
        hashed_password = hash_password(user.password)
        if(hash_password):

            user.password = hashed_password
        db_user = Users(name=user.name, email=user.email, password=user.password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        # generate token 
        user_db = db.query(Users).filter(Users.email == user.email).first()
   
        access_token = create_access_token(data={"user_email": user_db.email, "user_id": user_db.id, "user_name": user_db.name})
        return {
            "message": "User created successfully",
            "data": db_user,
            "access_token": access_token,
            "status": "success"
        }
    except Exception as e:
        return {
            "status": "error",
            "error": "Error creating user",
            "details": str(e)
        }
    
@user_router.get("/login", dependencies=[Depends(verify_api_key)])
def login(l_user:LoginUser, db: Session = Depends(get_db)):
    try:
        user = db.query(Users).filter(Users.email == l_user.email).first()
        is_equal = verify_password(l_user.password,user.password)
        print("is equal the both password", is_equal)
        if user and is_equal:
            access_token =create_access_token(data={"user_email": user.email, "user_id": user.id, "user_name": user.name})
            return {
                "access_token": access_token,
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email
                },

                "token_type": "bearer"}
            
        else:
            return {
                "error": "Invalid email or password",
                "status": "error"
            }
    except Exception as e:
        return {
            "error": "Error during login",
            "details": str(e)
        }
