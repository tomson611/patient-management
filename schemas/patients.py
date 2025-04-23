from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date

class PatientBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: str
    gender: str
    address: str
    phone_number: str
    email: EmailStr
    medical_history: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int
    is_active: bool


    class Config:
        from_attributes = True 