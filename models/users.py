"""SQLAlchemy model for User."""

from sqlalchemy import Boolean, Column, Integer, String

from db.database import Base


class User(Base):
    """SQLAlchemy User model."""

    __tablename__ = "users"

    username = Column(String, unique=True)
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
