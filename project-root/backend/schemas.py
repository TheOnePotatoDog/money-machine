from pydantic import BaseModel, EmailStr
from typing import Literal

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class LoginInput(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    credits: int
    class Config:
        orm_mode = True

class AIQuery(BaseModel):
    prompt: str
    agent: Literal["money", "safety"]
