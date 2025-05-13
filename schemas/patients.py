"""Pydantic schemas for patient-related data."""

from pydantic import BaseModel, EmailStr


class PatientBase(BaseModel):
    """Base schema for patient data."""

    first_name: str
    last_name: str
    date_of_birth: str
    gender: str
    address: str
    phone_number: str
    email: EmailStr
    medical_history: str | None = None


class PatientCreate(PatientBase):
    """Schema for creating a patient."""

    pass


class PatientResponse(PatientBase):
    """Schema for patient response data."""

    id: int
    is_active: bool

    class Config:
        """Pydantic configuration for ORM mode."""

        from_attributes = True
