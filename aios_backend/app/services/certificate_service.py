from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.models.certificate import Certificate


def validate_certificate_data(
    course_name: str,
    organization: str,
    issued_date: str,
    expiry_date: str = None,
) -> tuple:
    """
    Validate certificate metadata
    Returns: (is_valid, error_message)
    """
    errors = []
    
    # Validate course name
    if not course_name or len(course_name.strip()) == 0:
        errors.append("Course name is required")
    
    # Validate organization
    if not organization or len(organization.strip()) == 0:
        errors.append("Organization is required")
    
    # Validate dates
    try:
        issued_dt = datetime.strptime(issued_date, "%Y-%m-%d")
    except (ValueError, TypeError):
        errors.append("Invalid issued date format (use YYYY-MM-DD)")
        issued_dt = None
    
    if expiry_date:
        try:
            expiry_dt = datetime.strptime(expiry_date, "%Y-%m-%d")
            if issued_dt and expiry_dt < issued_dt:
                errors.append("Expiry date must be after issued date")
        except (ValueError, TypeError):
            errors.append("Invalid expiry date format (use YYYY-MM-DD)")
    
    is_valid = len(errors) == 0
    error_message = " | ".join(errors) if errors else None
    
    return is_valid, error_message


def upload_certificate(
    db: Session,
    student_id: int,
    course_name: str,
    organization: str,
    issued_date: str,
    expiry_date: str = None,
    certificate_url: str = None,
    notes: str = None,
) -> Certificate:
    """Upload and store certificate metadata"""
    
    # Validate input
    is_valid, error_message = validate_certificate_data(
        course_name, organization, issued_date, expiry_date
    )
    
    if not is_valid:
        raise ValueError(error_message)
    
    # Parse dates
    issued_dt = datetime.strptime(issued_date, "%Y-%m-%d").date()
    expiry_dt = None
    if expiry_date:
        expiry_dt = datetime.strptime(expiry_date, "%Y-%m-%d").date()
    
    # Create certificate record
    certificate = Certificate(
        student_id=student_id,
        course_name=course_name,
        organization=organization,
        issued_date=issued_dt,
        expiry_date=expiry_dt,
        certificate_url=certificate_url,
        verification_status="pending",
        notes=notes,
    )
    
    db.add(certificate)
    db.commit()
    db.refresh(certificate)
    
    return certificate


def get_student_certificates(db: Session, student_id: int) -> List[Certificate]:
    """Get all certificates for a student"""
    return db.query(Certificate).filter(
        Certificate.student_id == student_id
    ).order_by(Certificate.created_at.desc()).all()


def get_certificate_by_id(db: Session, certificate_id: int) -> Certificate:
    """Get certificate by ID"""
    return db.query(Certificate).filter(
        Certificate.id == certificate_id
    ).first()


def verify_certificate(db: Session, certificate_id: int, status: str, notes: str = None) -> Certificate:
    """Verify/reject a certificate (admin endpoint)"""
    if status not in ["verified", "rejected"]:
        raise ValueError("Status must be 'verified' or 'rejected'")
    
    certificate = get_certificate_by_id(db, certificate_id)
    if not certificate:
        raise ValueError(f"Certificate {certificate_id} not found")
    
    certificate.verification_status = status
    if notes:
        certificate.notes = notes
    
    db.add(certificate)
    db.commit()
    db.refresh(certificate)
    
    return certificate


def get_verified_certificates(db: Session, student_id: int) -> List[Certificate]:
    """Get verified certificates for a student"""
    return db.query(Certificate).filter(
        Certificate.student_id == student_id,
        Certificate.verification_status == "verified"
    ).all()
