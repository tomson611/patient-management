import pytest
from sqlalchemy.orm import Session
from sqlalchemy import text
from db.database import Base

def test_db_connection(db_session):
    """
    Test that the database connection is working
    """
    assert db_session is not None
    assert isinstance(db_session, Session)

def test_db_tables(setup_test_db, db_session):
    """
    Test that all tables are created in the database
    """
    # Get all table names from metadata
    table_names = Base.metadata.tables.keys()

    # Check that the expected tables exist
    assert 'users' in table_names
    assert 'patients' in table_names
    assert 'patient_user_assignments' in table_names

    # Check that we can execute a query
    result = db_session.execute(text("SELECT 1")).scalar()
    assert result == 1
