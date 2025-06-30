from fastapi import APIRouter, HTTPException, Depends
from validation.validation import auth_login, auth_register, auth_otp
from config.dataBase import db
from utils.utils import create_access_token, verify_password, hash_password, generate_otp,send_otp_email




auth_router = APIRouter()
@auth_router.post("/login")
async def login(user:auth_login):
    try:
        user_data = db.users.find_one({"email": user.email})
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not verify_password(user.password, user_data['password']):
            raise HTTPException(status_code=401, detail="Incorrect password")
        
        access_token = create_access_token(data={"user_id": str(user_data['_id']), "user_email": user_data['email'],"user_name":user_data['first_name']})

        return {
            "data": {
                "user_id": str(user_data['_id']),
                "user_email": user_data['email'],
                "user_name": user_data['first_name'],
                "access_token": access_token
            },
            "message": "Login successful",
            "status": "success"
        }
    except Exception as e:
        return {
            "data": None,
            "message": str(e),
            "status": "error"
        }
@auth_router.post("/otp")
async def otp(user: auth_otp):
    try:
        user_email = db.users.find_one({"email": user.email})
        if user_email:
            raise HTTPException(status_code=400, detail="Email already registered")
        
            
        otp_code = generate_otp()
        print("the otp code is ",otp_code)
        # Store the OTP in the database or cache with an expiration time
        db.otp_codes.insert_one({"email":user.email, "otp_code": otp_code})
        await send_otp_email(user.email, otp_code)
        print("email send not have any error ")

        return {
            "data": {
                "otp_code": otp_code
            },
            "message": "OTP sent successfully",
            "status": "success"
        }
    except Exception as e:
        return {
            "data": None,
            "message": str(e),
            "status": "error"
        }   
@auth_router.post("/register")
async def register(user: auth_register):
    try:
        existing_user = db.users.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        if not user.otp:
            raise HTTPException(status_code=400, detail="OTP is required for registration")
        otp_record = db.otp_codes.find_one({"email": user.email, "otp_code": user.otp})
        if not otp_record:
            raise HTTPException(status_code=400, detail="Invalid or expired OTP")
        # Remove the OTP record after successful verification
        db.otp_codes.delete_one({"email": user.email, "otp_code": user.otp})
        hashed_password = hash_password(user.password)
        new_user = {
            "email": user.email,
            "password": hashed_password,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone_number": user.phone_number
        }
        
        result = db.users.insert_one(new_user)
        
        access_token = create_access_token(data={"user_id": str(result.inserted_id), "user_email": user.email,"user_name":user.first_name})

        return {
            "data": {
                "user_id": str(result.inserted_id),
                "user_email": user.email,
                "user_name": user.first_name,
                "access_token": access_token
            },
            "message": "Registration successful",
            "status": "success"
        }
    except Exception as e:
        return {
            "data": None,
            "message": str(e),
            "status": "error"
        }

