from db.database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(String)
    gender = Column(String)
    address = Column(String)
    phone_number = Column(String)
    email = Column(String, unique=True)
    medical_history = Column(String)
    is_active = Column(Boolean, default=True)

