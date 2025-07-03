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
    otp: int | None = None
class auth_otp(BaseModel):
    email: str    

class AirlineAgentContext(BaseModel):
    passenger_name: str | None = None
    confirmation_number: str | None = None
    seat_number: str | None = None
    flight_number: str | None = None
    login_user_id: str | None = None  # Optional user ID for tracking

    