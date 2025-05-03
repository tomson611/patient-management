import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models.users import User

def test_register_user_success(client: TestClient, db_session: Session):
    """
    Test successful user registration
    """
    # Create a new user
    response = client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": "password123",
            "role": "user"
        }
    )
    
    # Check response
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "newuser@example.com"
    assert data["first_name"] == "New"
    assert data["last_name"] == "User"
    assert data["role"] == "user"
    assert data["is_active"] is True
    assert "id" in data
    
    # Check that user was created in the database
    user = db_session.query(User).filter(User.username == "newuser").first()
    assert user is not None
    assert user.email == "newuser@example.com"

def test_register_user_duplicate_username(client: TestClient, test_user: User):
    """
    Test registration with duplicate username
    """
    # Try to create a user with the same username
    response = client.post(
        "/auth/register",
        json={
            "username": test_user.username,  # Same username as test_user
            "email": "different@example.com",
            "first_name": "Different",
            "last_name": "User",
            "password": "password123",
            "role": "user"
        }
    )
    
    # Check response
    assert response.status_code == 400
    assert "Username already exists" in response.json()["detail"]

def test_register_user_duplicate_email(client: TestClient, test_user: User):
    """
    Test registration with duplicate email
    """
    # Try to create a user with the same email
    response = client.post(
        "/auth/register",
        json={
            "username": "differentuser",
            "email": test_user.email,  # Same email as test_user
            "first_name": "Different",
            "last_name": "User",
            "password": "password123",
            "role": "user"
        }
    )
    
    # Check response
    assert response.status_code == 400
    assert "Email already exists" in response.json()["detail"]

def test_register_user_invalid_data(client: TestClient):
    """
    Test registration with invalid data
    """
    # Try to create a user with invalid data
    response = client.post(
        "/auth/register",
        json={
            "username": "u",  # Too short
            "email": "not-an-email",  # Invalid email
            "first_name": "New",
            "last_name": "User",
            "password": "short",  # Too short
            "role": "invalid_role"  # Invalid role
        }
    )
    
    # Check response
    assert response.status_code == 422  # Validation error
    errors = response.json()["detail"]
    
    # Check that all validation errors are reported
    error_fields = [error["loc"][1] for error in errors]
    assert "username" in error_fields
    assert "email" in error_fields
    assert "password" in error_fields
    assert "role" in error_fields

def test_login_success(client: TestClient, test_user: User, db_session: Session):
    """
    Test successful login
    """
    # Update the test user's password to a known value
    from services.auth_service import bcrypt_context
    password = "testpassword"
    test_user.hashed_password = bcrypt_context.hash(password)
    db_session.commit()
    
    # Login with correct credentials
    response = client.post(
        "/auth/login",
        data={"username": test_user.username, "password": password}
    )
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client: TestClient, test_user: User, db_session: Session):
    """
    Test login with invalid credentials
    """
    # Update the test user's password to a known value
    from services.auth_service import bcrypt_context
    password = "testpassword"
    test_user.hashed_password = bcrypt_context.hash(password)
    db_session.commit()
    
    # Login with wrong password
    response = client.post(
        "/auth/login",
        data={"username": test_user.username, "password": "wrongpassword"}
    )
    
    # Check response
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]
    
    # Login with nonexistent username
    response = client.post(
        "/auth/login",
        data={"username": "nonexistentuser", "password": password}
    )
    
    # Check response
    assert response.status_code == 401
    assert "Invalid credentials" in response.json()["detail"]