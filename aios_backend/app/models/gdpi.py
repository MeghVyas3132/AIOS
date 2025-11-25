from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from datetime import datetime
from .base import Base


class GDPIQuestion(Base):
    __tablename__ = "gdpi_questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)  # e.g., "technical", "hr", "behavioral"
    difficulty = Column(String(50), default="medium", nullable=False)
    keywords = Column(Text, nullable=False)  # JSON list of keywords for scoring
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<GDPIQuestion(id={self.id}, category={self.category})>"


class GDPIResponse(Base):
    __tablename__ = "gdpi_responses"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("gdpi_questions.id"), nullable=False)
    response_text = Column(Text, nullable=False)
    score = Column(Float, nullable=False)  # 0-10 scale
    keywords_matched = Column(Text, nullable=True)  # JSON list of matched keywords
    feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<GDPIResponse(id={self.id}, student_id={self.student_id}, score={self.score})>"
