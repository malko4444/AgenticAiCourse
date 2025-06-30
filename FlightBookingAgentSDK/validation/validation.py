from pydantic import BaseModel



class auth_login(BaseModel):
    email: str
    password: str

class auth_register(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    phone_number: str | None = None
    otp: str | None = None
class auth_otp(BaseModel):
    email: str    
    