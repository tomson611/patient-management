"""API endpoints for patient management."""

import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from db.database import get_db
from models.patients import Patient
from models.users import User
from schemas.patients import PatientCreate, PatientResponse
from services.auth_service import get_current_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/patients", tags=["patients"])


@router.post(
    "/",
    response_model=PatientResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {
            "description": ("Bad Request - Invalid input data or email already exists")
        },
        404: {"description": "Not Found - User not found"},
        500: {"description": "Internal Server Error - Database error"},
    },
)
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Patient:
    """Create a new patient in the database."""
    try:
        db_patient = db.query(Patient).filter(Patient.email == patient.email).first()
        if db_patient:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        db_patient = Patient(**patient.model_dump())
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)

        return db_patient

    except IntegrityError as e:
        db.rollback()
        logger.error(f"Database integrity error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error occurred",
        )
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request",
        )
    except Exception as e:
        db.rollback()
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )


@router.get(
    "/{patient_id}",
    response_model=PatientResponse,
    responses={
        403: {"description": ("Forbidden - User doesn't have access to this patient")},
        404: {"description": "Not Found - Patient not found"},
        500: {"description": "Internal Server Error - Database error"},
    },
)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Patient:
    """Retrieve a patient by ID."""
    try:
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found",
            )

        return patient

    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the patient",
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )


@router.get(
    "/",
    response_model=List[PatientResponse],
    responses={500: {"description": "Internal Server Error - Database error"}},
)
def get_patients(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[Patient]:
    """Retrieve a list of patients."""
    try:
        patients = db.query(Patient).offset(skip).limit(limit).all()
        return patients

    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving patients",
        )
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )


@router.put(
    "/{patient_id}",
    response_model=PatientResponse,
    responses={
        400: {
            "description": ("Bad Request - Invalid input data or email already exists")
        },
        404: {"description": "Not Found - Patient or user not found"},
        500: {"description": "Internal Server Error - Database error"},
    },
)
def update_patient(
    patient_id: int,
    patient: PatientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Patient:
    """Update an existing patient."""
    try:
        db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not db_patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found",
            )

        if patient.email != db_patient.email:
            existing_patient = (
                db.query(Patient).filter(Patient.email == patient.email).first()
            )
            if existing_patient:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )

        for key, value in patient.model_dump().items():
            setattr(db_patient, key, value)

        db.commit()
        db.refresh(db_patient)
        return db_patient

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the patient",
        )
    except Exception as e:
        db.rollback()
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )


@router.delete(
    "/{patient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        403: {"description": "Forbidden - Only admin users can delete patients"},
        404: {"description": "Not Found - Patient not found"},
        500: {"description": "Internal Server Error - Database error"},
    },
)
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    """Delete a patient from the database."""
    try:
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only admin users can delete patients",
            )

        db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not db_patient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Patient not found",
            )

        db.delete(db_patient)
        db.commit()

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the patient",
        )
    except Exception as e:
        db.rollback()
        if isinstance(e, HTTPException):
            raise e
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )
