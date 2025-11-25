from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from datetime import datetime
from .base import Base


class PlacementProfile(Base):
    __tablename__ = "placement_profiles"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    skills = Column(Text, nullable=False)  # JSON list of skills
    projects = Column(Text, nullable=True)  # JSON list of projects
    cgpa = Column(Float, nullable=False)
    experience = Column(String(255), nullable=True)  # Years of experience
    best_fit_domain = Column(String(100), nullable=True)  # e.g., "Web", "ML", "Cloud", "Cybersecurity"
    domain_scores = Column(Text, nullable=True)  # JSON dict of domain scores
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<PlacementProfile(id={self.id}, student_id={self.student_id}, domain={self.best_fit_domain})>"
