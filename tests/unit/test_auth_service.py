import pytest
from datetime import timedelta
from jose import jwt
from fastapi import HTTPException

from services.auth_service import (
    authenticate_user,
    create_access_token,
    get_current_user,
    bcrypt_context
)
from config import settings

def test_authenticate_user_success(db_session, test_user):
    """
    Test successful user authentication
    """
    # Update the test user's password to a known value
    password = "testpassword"
    hashed_password = bcrypt_context.hash(password)
    test_user.hashed_password = hashed_password
    db_session.commit()
    
    # Authenticate with correct credentials
    authenticated_user = authenticate_user(test_user.username, password, db_session)
    
    # Check that authentication succeeded
    assert authenticated_user is not None
    assert authenticated_user.id == test_user.id
    assert authenticated_user.username == test_user.username

def test_authenticate_user_wrong_password(db_session, test_user):
    """
    Test authentication with wrong password
    """
    # Update the test user's password to a known value
    password = "testpassword"
    hashed_password = bcrypt_context.hash(password)
    test_user.hashed_password = hashed_password
    db_session.commit()
    
    # Authenticate with wrong password
    authenticated_user = authenticate_user(test_user.username, "wrongpassword", db_session)
    
    # Check that authentication failed
    assert authenticated_user is False

def test_authenticate_user_nonexistent_user(db_session):
    """
    Test authentication with nonexistent user
    """
    # Authenticate with nonexistent username
    authenticated_user = authenticate_user("nonexistentuser", "password", db_session)
    
    # Check that authentication failed
    assert authenticated_user is False

def test_create_access_token():
    """
    Test creating an access token
    """
    # Create a token
    username = "testuser"
    user_id = "1"
    role = "user"
    expires_delta = timedelta(minutes=15)
    
    token = create_access_token(username, user_id, role, expires_delta)
    
    # Decode the token and verify its contents
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    
    assert payload["sub"] == username
    assert payload["id"] == user_id
    assert payload["role"] == role
    assert "exp" in payload  # Expiration time should be set

@pytest.mark.asyncio
async def test_get_current_user_valid_token(user_token):
    """
    Test getting current user with a valid token
    """
    # Get current user with valid token
    user = await get_current_user(user_token)
    
    # Check that user info is returned
    assert user is not None
    assert "username" in user
    assert "id" in user
    assert "role" in user
    assert user["role"] == "user"

@pytest.mark.asyncio
async def test_get_current_user_invalid_token():
    """
    Test getting current user with an invalid token
    """
    # Try to get current user with invalid token
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user("invalid_token")
    
    # Check that the correct exception is raised
    assert excinfo.value.status_code == 401
    assert "Invalid token" in excinfo.value.detail

@pytest.mark.asyncio
async def test_get_current_user_missing_claims():
    """
    Test getting current user with a token missing required claims
    """
    # Create a token with missing claims
    token = jwt.encode(
        {"some_claim": "value"},  # Missing 'sub' and 'id'
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    
    # Try to get current user with this token
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token)
    
    # Check that the correct exception is raised
    assert excinfo.value.status_code == 401
    assert "Invalid credentials" in excinfo.value.detail