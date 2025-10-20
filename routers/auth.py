"""API endpoints for authentication and user management."""

import logging
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config import settings
from db.database import get_db
from models.users import User
from schemas.users import Token, UserCreate, UserResponse
from services.auth_service import authenticate_user, bcrypt_context, create_access_token
from services.auth_service import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])
db_dependency = Annotated[Session, Depends(get_db)]
logger = logging.getLogger(__name__)


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
    responses={
        400: {"description": ("Bad Request (Email or Username already exists)")},
        500: {"description": "Internal Server Error"},
    },
)
async def create_user(user_create: UserCreate, db: db_dependency) -> UserResponse:
    """Create a new user in the database."""
    try:
        hashed_password = bcrypt_context.hash(user_create.password)
        user = User(
            email=user_create.email,
            username=user_create.username,
            hashed_password=hashed_password,
            role=user_create.role,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return UserResponse.model_validate(user, from_attributes=True)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)
        logger.error("IntegrityError: %s", error_message)

        if "email" in error_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )
        elif "username" in error_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Database constraint error",
            )
    except Exception as e:
        db.rollback()
        logger.exception("An unexpected error occurred: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.post(
    "/login",
    response_model=Token,
    responses={401: {"description": "Invalid credentials"}},
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency,
) -> dict:
    """Authenticate user and return an access token."""
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        username=str(user.username),
        user_id=str(user.id),
        role=str(user.role),
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}




@router.get(
    "/me",
    response_model=UserResponse,
    responses={401: {"description": "Unauthorized"}},
)
async def read_current_user(current_user: User = Depends(get_current_user)) -> UserResponse:
    """Return information about the currently authenticated user."""
    return UserResponse.model_validate(current_user, from_attributes=True)
