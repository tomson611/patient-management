import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database
from fastapi.testclient import TestClient
from datetime import timedelta

from db.database import Base, get_db
from main import app
from models.users import User
from models.patients import Patient
from services.auth_service import bcrypt_context, create_access_token

# Test database URL
TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/test_patient_management"

# Create test engine
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"port": 5433})

# Create test session
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture(scope="session")
def setup_test_db():
    """
    Create a test database, set up tables, and tear down after tests
    """
    # Create test database if it doesn't exist
    if not database_exists(TEST_DATABASE_URL):
        create_database(TEST_DATABASE_URL)

    # Create tables
    Base.metadata.create_all(bind=test_engine)

    yield

    # Drop test database after tests
    drop_database(TEST_DATABASE_URL)

@pytest.fixture
def db_session(setup_test_db):
    """
    Create a fresh database session for each test
    """
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    """
    Create a test client with a test database session
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # Reset dependency override
    app.dependency_overrides = {}

@pytest.fixture
def test_user(db_session):
    """
    Create a test user for authentication tests
    """
    user = User(
        username="testuser",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        hashed_password=bcrypt_context.hash("password123"),
        is_active=True,
        role="user"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def test_admin(db_session):
    """
    Create a test admin user for authorization tests
    """
    admin = User(
        username="testadmin",
        email="admin@example.com",
        first_name="Test",
        last_name="Admin",
        hashed_password=bcrypt_context.hash("password123"),
        is_active=True,
        role="admin"
    )
    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)
    return admin

@pytest.fixture
def user_token(test_user):
    """
    Create a token for the test user
    """
    return create_access_token(
        username=test_user.username,
        user_id=str(test_user.id),
        role=test_user.role,
        expires_delta=timedelta(minutes=30)
    )

@pytest.fixture
def admin_token(test_admin):
    """
    Create a token for the test admin
    """
    return create_access_token(
        username=test_admin.username,
        user_id=str(test_admin.id),
        role=test_admin.role,
        expires_delta=timedelta(minutes=30)
    )

@pytest.fixture
def user_headers(user_token):
    """
    Create headers with user token for authenticated requests
    """
    return {"Authorization": f"Bearer {user_token}"}

@pytest.fixture
def admin_headers(admin_token):
    """
    Create headers with admin token for authenticated requests
    """
    return {"Authorization": f"Bearer {admin_token}"}

@pytest.fixture
def test_patient(db_session):
    """
    Create a test patient for patient tests
    """
    patient = Patient(
        first_name="Test",
        last_name="Patient",
        date_of_birth="1990-01-01",
        gender="Male",
        address="123 Test St",
        phone_number="123-456-7890",
        email="testpatient@example.com",
        medical_history="No significant medical history",
        is_active=True
    )
    db_session.add(patient)
    db_session.commit()
    db_session.refresh(patient)
    return patient
