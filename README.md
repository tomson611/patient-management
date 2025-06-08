# Patient Management System

A FastAPI-based application for managing patient records. This system provides a secure API for creating, retrieving, updating, and deleting patient information, with user authentication and role-based access control.

## Features

- **User Authentication:** Secure user registration and login with JWT access tokens.
- **Patient Management:** CRUD operations for patient records.
- **Role-Based Access:** Differentiated access levels (e.g., admin-only actions).
- **Relational Database:** Uses PostgreSQL for data persistence with SQLAlchemy ORM.
- **Dependency Management:** Managed with Poetry for reproducible environments.
- **Pre-commit Hooks:** Ensures code quality and consistency.

## Technologies Used

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/)
- **Database:** [PostgreSQL](https://www.postgresql.org/)
- **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
- **Authentication:** [python-jose](https://github.com/mpdavis/python-jose) for JWT
- **Environment Management:** [Poetry](https://python-poetry.org/)
- **Code Formatting & Linting:** [Ruff](https://github.com/astral-sh/ruff), [Mypy](http://mypy-lang.org/)

## Setup and Installation

### Prerequisites

-   [Python 3.10+](https://www.python.org/downloads/)
-   [Poetry](https://python-poetry.org/docs/#installation)
-   [PostgreSQL](https://www.postgresql.org/download/) running on your system.

### 1. Clone the Repository

```bash
git clone <repository-url>
cd patient-management
```

### 2. Install Dependencies

This project uses Poetry for dependency management. Install the project dependencies by running:

```bash
poetry install
```

This will create a virtual environment and install all necessary packages.

### 3. Configure Environment Variables

Create a `.env` file in the project root directory. You can copy the example below and replace the placeholder values with your actual configuration.

```env
# .env

# A long, random, and secret string. You can generate one with: openssl rand -hex 32
SECRET_KEY='your_super_secret_key'

# The algorithm used for JWT encoding
ALGORITHM='HS256'

# Database connection string
# Format: postgresql://<user>:<password>@<host>:<port>/<dbname>
DATABASE_URL='postgresql://user:password@localhost:5432/patient_db'

# Access token lifetime in minutes
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Database Setup

The application is configured to automatically create the necessary database tables on startup. Ensure your PostgreSQL server is running and that the database specified in your `DATABASE_URL` exists.

## Running the Application

To start the FastAPI application, run the following command from the project root:

```bash
poetry run start
```

The application will be available at `http://localhost:8001`. You can access the interactive API documentation at `http://localhost:8001/docs`.

## Running Tests

To run the test suite, use `pytest`:

```bash
poetry run pytest
```

## API Endpoints

### Authentication (`/auth`)

-   `POST /auth/register`: Create a new user.
-   `POST /auth/login`: Authenticate a user and receive a JWT access token.

### Patients (`/patients`)

-   `POST /patients/`: Create a new patient.
-   `GET /patients/`: Retrieve a list of all patients.
-   `GET /patients/{patient_id}`: Retrieve a specific patient by their ID.
-   `PUT /patients/{patient_id}`: Update a patient's information.
-   `DELETE /patients/{patient_id}`: Delete a patient (Admin only).
