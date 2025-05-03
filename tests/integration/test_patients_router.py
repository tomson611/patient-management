import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from models.patients import Patient
from models.users import User

def test_create_patient_admin(client: TestClient, admin_headers: dict, db_session: Session):
    """
    Test creating a patient as an admin
    """
    # Create a patient
    response = client.post(
        "/patients/",
        headers=admin_headers,
        json={
            "first_name": "New",
            "last_name": "Patient",
            "date_of_birth": "1995-05-15",
            "gender": "Female",
            "address": "456 Test Ave",
            "phone_number": "987-654-3210",
            "email": "newpatient@example.com",
            "medical_history": "Allergies to peanuts",
            "assigned_user_ids": []
        }
    )
    
    # Check response
    assert response.status_code == 201
    data = response.json()
    assert data["first_name"] == "New"
    assert data["last_name"] == "Patient"
    assert data["date_of_birth"] == "1995-05-15"
    assert data["gender"] == "Female"
    assert data["address"] == "456 Test Ave"
    assert data["phone_number"] == "987-654-3210"
    assert data["email"] == "newpatient@example.com"
    assert data["medical_history"] == "Allergies to peanuts"
    assert data["is_active"] is True
    assert "id" in data
    assert len(data["assigned_users"]) == 1  # Admin user is automatically assigned
    
    # Check that patient was created in the database
    patient = db_session.query(Patient).filter(Patient.email == "newpatient@example.com").first()
    assert patient is not None
    assert patient.first_name == "New"
    assert len(patient.assigned_users) == 1

def test_create_patient_regular_user(client: TestClient, user_headers: dict):
    """
    Test that regular users cannot create patients
    """
    # Try to create a patient as a regular user
    response = client.post(
        "/patients/",
        headers=user_headers,
        json={
            "first_name": "New",
            "last_name": "Patient",
            "date_of_birth": "1995-05-15",
            "gender": "Female",
            "address": "456 Test Ave",
            "phone_number": "987-654-3210",
            "email": "newpatient2@example.com",
            "medical_history": "None",
            "assigned_user_ids": []
        }
    )
    
    # Check response
    assert response.status_code == 403
    assert "Only admin users can create patients" in response.json()["detail"]

def test_create_patient_duplicate_email(client: TestClient, admin_headers: dict, test_patient: Patient):
    """
    Test creating a patient with a duplicate email
    """
    # Try to create a patient with the same email
    response = client.post(
        "/patients/",
        headers=admin_headers,
        json={
            "first_name": "Duplicate",
            "last_name": "Email",
            "date_of_birth": "1990-01-01",
            "gender": "Male",
            "address": "123 Test St",
            "phone_number": "123-456-7890",
            "email": test_patient.email,  # Same email as test_patient
            "medical_history": "None",
            "assigned_user_ids": []
        }
    )
    
    # Check response
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_get_patient_admin(client: TestClient, admin_headers: dict, test_patient: Patient):
    """
    Test getting a patient as an admin
    """
    # Get the patient
    response = client.get(
        f"/patients/{test_patient.id}",
        headers=admin_headers
    )
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_patient.id
    assert data["first_name"] == test_patient.first_name
    assert data["last_name"] == test_patient.last_name
    assert data["email"] == test_patient.email

def test_get_patient_assigned_user(client: TestClient, user_headers: dict, test_patient: Patient, test_user: User, db_session: Session):
    """
    Test getting a patient as an assigned user
    """
    # Assign the test user to the patient
    test_patient.assigned_users.append(test_user)
    db_session.commit()
    
    # Get the patient
    response = client.get(
        f"/patients/{test_patient.id}",
        headers=user_headers
    )
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == test_patient.id
    assert data["first_name"] == test_patient.first_name

def test_get_patient_unassigned_user(client: TestClient, user_headers: dict, test_patient: Patient):
    """
    Test that unassigned users cannot get a patient
    """
    # Try to get the patient as an unassigned user
    response = client.get(
        f"/patients/{test_patient.id}",
        headers=user_headers
    )
    
    # Check response
    assert response.status_code == 403
    assert "You don't have access to this patient's information" in response.json()["detail"]

def test_get_patients_admin(client: TestClient, admin_headers: dict, test_patient: Patient):
    """
    Test getting all patients as an admin
    """
    # Get all patients
    response = client.get(
        "/patients/",
        headers=admin_headers
    )
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1  # At least the test patient
    
    # Check that the test patient is in the list
    patient_ids = [p["id"] for p in data]
    assert test_patient.id in patient_ids

def test_get_patients_regular_user(client: TestClient, user_headers: dict, test_patient: Patient, test_user: User, db_session: Session):
    """
    Test getting patients as a regular user
    """
    # Assign the test user to the patient
    test_patient.assigned_users.append(test_user)
    db_session.commit()
    
    # Get patients
    response = client.get(
        "/patients/",
        headers=user_headers
    )
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1  # Only the assigned patient
    assert data[0]["id"] == test_patient.id

def test_update_patient_admin(client: TestClient, admin_headers: dict, test_patient: Patient, db_session: Session):
    """
    Test updating a patient as an admin
    """
    # Update the patient
    response = client.put(
        f"/patients/{test_patient.id}",
        headers=admin_headers,
        json={
            "first_name": "Updated",
            "last_name": "Patient",
            "date_of_birth": test_patient.date_of_birth,
            "gender": test_patient.gender,
            "address": test_patient.address,
            "phone_number": test_patient.phone_number,
            "email": test_patient.email,
            "medical_history": "Updated medical history",
            "assigned_user_ids": []
        }
    )
    
    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Updated"
    assert data["last_name"] == "Patient"
    assert data["medical_history"] == "Updated medical history"
    
    # Check that patient was updated in the database
    db_session.refresh(test_patient)
    assert test_patient.first_name == "Updated"
    assert test_patient.medical_history == "Updated medical history"

def test_update_patient_regular_user(client: TestClient, user_headers: dict, test_patient: Patient):
    """
    Test that regular users cannot update patients
    """
    # Try to update the patient as a regular user
    response = client.put(
        f"/patients/{test_patient.id}",
        headers=user_headers,
        json={
            "first_name": "Unauthorized",
            "last_name": "Update",
            "date_of_birth": test_patient.date_of_birth,
            "gender": test_patient.gender,
            "address": test_patient.address,
            "phone_number": test_patient.phone_number,
            "email": test_patient.email,
            "medical_history": "Unauthorized update",
            "assigned_user_ids": []
        }
    )
    
    # Check response
    assert response.status_code == 403
    assert "Only admin users can edit patients" in response.json()["detail"]

def test_delete_patient_admin(client: TestClient, admin_headers: dict, db_session: Session):
    """
    Test deleting a patient as an admin
    """
    # Create a patient to delete
    patient = Patient(
        first_name="Delete",
        last_name="Me",
        date_of_birth="2000-01-01",
        gender="Other",
        address="Delete Address",
        phone_number="111-222-3333",
        email="delete@example.com",
        is_active=True
    )
    db_session.add(patient)
    db_session.commit()
    patient_id = patient.id
    
    # Delete the patient
    response = client.delete(
        f"/patients/{patient_id}",
        headers=admin_headers
    )
    
    # Check response
    assert response.status_code == 204
    
    # Check that patient was deleted from the database
    deleted_patient = db_session.query(Patient).filter(Patient.id == patient_id).first()
    assert deleted_patient is None

def test_delete_patient_regular_user(client: TestClient, user_headers: dict, test_patient: Patient):
    """
    Test that regular users cannot delete patients
    """
    # Try to delete the patient as a regular user
    response = client.delete(
        f"/patients/{test_patient.id}",
        headers=user_headers
    )
    
    # Check response
    assert response.status_code == 403
    assert "Only admin users can delete patients" in response.json()["detail"]

def test_delete_nonexistent_patient(client: TestClient, admin_headers: dict):
    """
    Test deleting a nonexistent patient
    """
    # Try to delete a nonexistent patient
    response = client.delete(
        "/patients/9999",  # Assuming this ID doesn't exist
        headers=admin_headers
    )
    
    # Check response
    assert response.status_code == 404
    assert "Patient not found" in response.json()["detail"]