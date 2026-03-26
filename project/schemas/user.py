from pydantic import BaseModel, EmailStr, Field
from typing import Optional
import datetime

# user base modal
class UserBase(BaseModel):
    name: str
    age: int
    email: EmailStr
    address: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now)


# user Input 
class UserCreate(UserBase):
    pass


# Output
class UserOutput(UserBase):
    id: int

    class Config:
        from_attributes = True