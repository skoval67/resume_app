from pydantic import ConfigDict, BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# Auth
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Resume
class ResumeCreate(BaseModel):
    title: str
    content: str

class ResumeUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class ResumeHistory(BaseModel):
    content: str

class ResumeOut(ResumeCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    improvements: List[ResumeHistory] = []
    model_config = ConfigDict(from_attributes=True)
