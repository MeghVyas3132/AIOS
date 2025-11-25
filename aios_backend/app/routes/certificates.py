from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.core.database import get_db
from app.core.deps import get_current_user, require_admin, require_student
from app.models.user import User
from app.models.certificate import Certificate
from app.schemas import CertificateCreate, CertificateResponse
from app.services.certificate_service import (
    upload_certificate, get_student_certificates,
    get_verified_certificates, verify_certificate, get_certificate_by_id
)

router = APIRouter(prefix="/api/certificates", tags=["Certificates"])


@router.post("/upload", response_model=CertificateResponse)
async def upload_certificate_endpoint(
    cert_data: CertificateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
):
    """
    Upload certificate metadata
    Validates certificate fields before storing
    """
    try:
        certificate = upload_certificate(
            db,
            student_id=current_user.id,
            course_name=cert_data.course_name,
            organization=cert_data.organization,
            issued_date=cert_data.issued_date,
            expiry_date=cert_data.expiry_date,
            certificate_url=cert_data.certificate_url,
            notes=cert_data.notes,
        )
        return certificate
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/my-certificates", response_model=List[CertificateResponse])
async def get_my_certificates(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
):
    """Get all certificates uploaded by the current student"""
    certificates = get_student_certificates(db, current_user.id)
    return certificates


@router.get("/my-verified", response_model=List[CertificateResponse])
async def get_my_verified_certificates(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
):
    """Get only verified certificates for the current student"""
    certificates = get_verified_certificates(db, current_user.id)
    return certificates


@router.get("/{certificate_id}", response_model=CertificateResponse)
async def get_certificate_details(
    certificate_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
):
    """Get details of a specific certificate"""
    certificate = get_certificate_by_id(db, certificate_id)
    
    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found",
        )
    
    # Ensure student can only see their own certificates
    if certificate.student_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have access to this certificate",
        )
    
    return certificate


@router.post("/verify/{certificate_id}", response_model=CertificateResponse)
async def verify_certificate_endpoint(
    certificate_id: int,
    status_update: str,
    notes: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Verify or reject a certificate (admin only)
    Status options: verified, rejected
    """
    try:
        certificate = verify_certificate(db, certificate_id, status_update, notes)
        return certificate
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get("/admin/pending", response_model=List[CertificateResponse])
async def get_pending_certificates(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Get all pending certificate verifications (admin only)"""
    certificates = db.query(Certificate).filter(
        Certificate.verification_status == "pending"
    ).all()
    return certificates
