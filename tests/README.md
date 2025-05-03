# Patient Management System Tests

This directory contains tests for the Patient Management System. The tests are organized into unit tests and integration tests.

## Test Structure

- `tests/unit/`: Contains unit tests for individual components
  - `test_database.py`: Tests for database connection and tables
  - `test_user_model.py`: Tests for the User model
  - `test_patient_model.py`: Tests for the Patient model
  - `test_auth_service.py`: Tests for authentication services

- `tests/integration/`: Contains integration tests for API endpoints
  - `test_auth_router.py`: Tests for authentication endpoints
  - `test_patients_router.py`: Tests for patient management endpoints

- `conftest.py`: Contains shared fixtures for all tests

## Prerequisites

Before running the tests, make sure you have installed the required dependencies:

```bash
pip install -r requirements.txt
pip install -r test_requirements.txt
```

## Running the Tests

To run all tests:

```bash
pytest
```

To run tests with coverage report:

```bash
pytest --cov=.
```

To run specific test files:

```bash
pytest tests/unit/test_database.py
pytest tests/integration/test_auth_router.py
```

## Test Database

The tests use a separate test database to avoid affecting the production database. The test database is created and dropped automatically during test execution.

The test database URL is configured in `conftest.py`:

```python
TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/test_patient_management"
```

Make sure you have PostgreSQL running on port 5433 with the specified credentials, or update the URL to match your environment.

## Test Users

The tests create the following test users:

1. Regular user:
   - Username: testuser
   - Email: test@example.com
   - Role: user

2. Admin user:
   - Username: testadmin
   - Email: admin@example.com
   - Role: admin

These users are created automatically by the test fixtures in `conftest.py`.

## Authentication in Tests

The tests use JWT tokens for authentication. The tokens are generated automatically by the test fixtures in `conftest.py`.

To make authenticated requests in tests, use the `user_headers` or `admin_headers` fixtures:

```python
def test_authenticated_endpoint(client, user_headers):
    response = client.get("/some-endpoint", headers=user_headers)
    assert response.status_code == 200
```