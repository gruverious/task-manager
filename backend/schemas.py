from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional


class UserRegister(BaseModel):
    username:str 
    email:EmailStr # for automatic email format validation
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int 
    username:str 
    email:EmailStr 

    class Config:
        from_attributes=True
    
class TaskCreate(BaseModel):
    title:str 
    description:Optional[str] = None

class TaskUpdate(BaseModel):
    completed:bool 

class TaskResponse(BaseModel):
    id:int
    title:str 
    description:Optional[str]=None
    completed:bool 
    created_at:datetime
    user_id:int

    class Config:
        from_attributes=True

class TokenResponse(BaseModel):
    access_token:str 
    token_type:str 

