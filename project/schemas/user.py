from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
import datetime

# user base modal
class UserBase(BaseModel):
    name: str
    age: int
    email: EmailStr
    address: Optional[str] = None
    phone: Optional[str] = None


# user Input 
class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    phone: Optional[str] = None

# Output
class UserOutput(UserBase):
    id: int
    created_at: datetime.datetime

  

    model_config = ConfigDict(from_attributes=True)