from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Date
from datetime import datetime, date
from .base import Base


class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_name = Column(String(255), nullable=False)
    organization = Column(String(255), nullable=False)
    issued_date = Column(Date, nullable=False)
    expiry_date = Column(Date, nullable=True)
    certificate_url = Column(Text, nullable=True)  # URL or file path
    verification_status = Column(String(50), default="pending", nullable=False)  # pending, verified, rejected
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Certificate(id={self.id}, course_name={self.course_name})>"
