import pytest
from sqlalchemy.exc import IntegrityError
from models.patients import Patient
from models.users import User

def test_create_patient(db_session):
    """
    Test creating a patient
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
    
    assert patient.id is not None
    assert patient.first_name == "Test"
    assert patient.last_name == "Patient"
    assert patient.date_of_birth == "1990-01-01"
    assert patient.gender == "Male"
    assert patient.address == "123 Test St"
    assert patient.phone_number == "123-456-7890"
    assert patient.email == "testpatient@example.com"
    assert patient.medical_history == "No significant medical history"
    assert patient.is_active is True

def test_unique_email_constraint(db_session):
    """
    Test that email must be unique
    """
    # Create first patient
    patient1 = Patient(
        first_name="Test1",
        last_name="Patient1",
        date_of_birth="1990-01-01",
        gender="Male",
        address="123 Test St",
        phone_number="123-456-7890",
        email="duplicate@example.com",
        is_active=True
    )
    db_session.add(patient1)
    db_session.commit()
    
    # Try to create a patient with the same email
    patient2 = Patient(
        first_name="Test2",
        last_name="Patient2",
        date_of_birth="1995-01-01",
        gender="Female",
        address="456 Test St",
        phone_number="987-654-3210",
        email="duplicate@example.com",  # Same email as patient1
        is_active=True
    )
    
    db_session.add(patient2)
    
    # Should raise an IntegrityError due to unique constraint
    with pytest.raises(IntegrityError):
        db_session.commit()
    
    # Rollback the failed transaction
    db_session.rollback()

def test_patient_user_relationship(db_session, test_user):
    """
    Test the many-to-many relationship between patients and users
    """
    # Create a patient
    patient = Patient(
        first_name="Relationship",
        last_name="Test",
        date_of_birth="1990-01-01",
        gender="Male",
        address="123 Test St",
        phone_number="123-456-7890",
        email="relationship@example.com",
        is_active=True
    )
    db_session.add(patient)
    db_session.commit()
    
    # Initially, the patient should have no assigned users
    assert len(patient.assigned_users) == 0
    
    # Assign the test user to the patient
    patient.assigned_users.append(test_user)
    db_session.commit()
    
    # Refresh both objects to ensure relationships are loaded
    db_session.refresh(patient)
    db_session.refresh(test_user)
    
    # Check that the relationship is established
    assert len(patient.assigned_users) == 1
    assert patient.assigned_users[0].id == test_user.id
    assert len(test_user.assigned_patients) == 1
    assert test_user.assigned_patients[0].id == patient.id
    
    # Test removing the relationship
    patient.assigned_users.remove(test_user)
    db_session.commit()
    
    # Refresh both objects
    db_session.refresh(patient)
    db_session.refresh(test_user)
    
    # Check that the relationship is removed
    assert len(patient.assigned_users) == 0
    assert len(test_user.assigned_patients) == 0