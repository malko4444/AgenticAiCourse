from pydantic import BaseModel
from typing import Optional
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    completed: Optional[bool] = False
    status: Optional[str] = None

class LoginUser(BaseModel):
    email:str
    password: str
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
