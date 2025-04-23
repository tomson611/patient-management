from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db.database import get_db
from models.users import User
from schemas.users import CreateUserRequest, UserResponse, Token
from config import settings
from services.auth_service import (
    authenticate_user,
    create_access_token,
    get_current_user,
    bcrypt_context,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)
db_dependency = Annotated[Session, Depends(get_db)]


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
    responses={
        400: {"description": "Bad Request (Email or Username already exists)"},
        500: {"description": "Internal Server Error"}
    }
)
async def create_user(
    create_user_request: CreateUserRequest,
    db: db_dependency
):
    hashed_password = bcrypt_context.hash(create_user_request.password)
    user = User(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=hashed_password,
        is_active=True
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError as e:
        db.rollback()
        error_message = str(e.orig)
        if "email" in error_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        elif "username" in error_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Database constraint error"
            )
    return user


@router.post(
    "/login",
    response_model=Token,
    responses={401: {"description": "Invalid credentials"}}
)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        username=user.username,
        user_id=str(user.id),
        role=user.role,
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
