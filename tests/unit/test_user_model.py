import pytest
from sqlalchemy.exc import IntegrityError
from models.users import User

def test_create_user(db_session):
    """
    Test creating a user
    """
    user = User(
        username="testuser1",
        email="testuser1@example.com",
        first_name="Test",
        last_name="User",
        hashed_password="hashedpassword",
        is_active=True,
        role="user"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    
    assert user.id is not None
    assert user.username == "testuser1"
    assert user.email == "testuser1@example.com"
    assert user.first_name == "Test"
    assert user.last_name == "User"
    assert user.hashed_password == "hashedpassword"
    assert user.is_active is True
    assert user.role == "user"

def test_unique_username_constraint(db_session, test_user):
    """
    Test that username must be unique
    """
    # Try to create a user with the same username
    duplicate_user = User(
        username=test_user.username,  # Same username as test_user
        email="different@example.com",
        first_name="Different",
        last_name="User",
        hashed_password="hashedpassword",
        is_active=True,
        role="user"
    )
    
    db_session.add(duplicate_user)
    
    # Should raise an IntegrityError due to unique constraint
    with pytest.raises(IntegrityError):
        db_session.commit()
    
    # Rollback the failed transaction
    db_session.rollback()

def test_unique_email_constraint(db_session, test_user):
    """
    Test that email must be unique
    """
    # Try to create a user with the same email
    duplicate_user = User(
        username="differentuser",
        email=test_user.email,  # Same email as test_user
        first_name="Different",
        last_name="User",
        hashed_password="hashedpassword",
        is_active=True,
        role="user"
    )
    
    db_session.add(duplicate_user)
    
    # Should raise an IntegrityError due to unique constraint
    with pytest.raises(IntegrityError):
        db_session.commit()
    
    # Rollback the failed transaction
    db_session.rollback()

def test_user_relationships(db_session, test_user):
    """
    Test that user relationships work correctly
    """
    # Initially, the user should have no assigned patients
    assert len(test_user.assigned_patients) == 0
    
    # We'll test adding patients in the patient model tests