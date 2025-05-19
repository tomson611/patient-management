"""Authentication service functions."""

from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config import settings
from db.database import get_db
from models.users import User

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def authenticate_user(username: str, password: str, db: Session) -> User | None:
    """Authenticate a user by username and password."""
    user = db.query(User).filter(User.username == username).first()
    if not user or not bcrypt_context.verify(password, str(user.hashed_password)):
        return None
    return user


def create_access_token(
    username: str, user_id: str, role: str, expires_delta: timedelta
) -> str:
    """Create a JWT access token for the user."""
    expire = datetime.now(timezone.utc) + expires_delta
    payload = {
        "sub": username,
        "id": user_id,
        "role": role,
        "exp": int(expire.timestamp()),  # Store as Unix timestamp
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """Get the current authenticated user from the JWT token."""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str | None = payload.get("sub")
        user_id: str | None = payload.get("id")
        user_role: str | None = payload.get("role")

        if any(x is None for x in (username, user_id, user_role)):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            user_id_int = int(user_id) if user_id is not None else None
            if user_id_int is None:
                raise ValueError("User ID is None")
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid user ID format",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = db.query(User).filter(User.id == user_id_int).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
