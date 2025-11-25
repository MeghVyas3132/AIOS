from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text
from datetime import datetime
from .base import Base


class WeakTopicReport(Base):
    __tablename__ = "weak_topic_reports"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    test_id = Column(Integer, ForeignKey("tests.id"), nullable=False)
    topic = Column(String(100), nullable=False)
    score = Column(Float, nullable=False)  # Percentage
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    is_weak = Column(Integer, default=0, nullable=False)  # 1 if below threshold
    threshold = Column(Float, default=70.0, nullable=False)
    recommendation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<WeakTopicReport(id={self.id}, topic={self.topic}, score={self.score})>"
