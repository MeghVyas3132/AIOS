from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    STUDENT = "student"
    FACULTY = "faculty"
    ADMIN = "admin"


# User Schemas
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.STUDENT


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole
    bio: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Test & Question Schemas
class QuestionBase(BaseModel):
    question_text: str
    topic: str
    correct_answer: str
    options: Optional[str] = None
    difficulty: str = "medium"


class QuestionCreate(QuestionBase):
    pass


class QuestionResponse(QuestionBase):
    id: int
    test_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class TestBase(BaseModel):
    title: str
    description: Optional[str] = None


class TestCreate(TestBase):
    questions: Optional[List[QuestionCreate]] = None


class TestResponse(TestBase):
    id: int
    created_by: int
    questions: List[QuestionResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Answer Schemas
class AnswerCreate(BaseModel):
    question_id: int
    student_answer: str


class StudentTestAnswerCreate(BaseModel):
    test_id: int
    answers: List[AnswerCreate]


class AnswerResponse(BaseModel):
    id: int
    question_id: int
    student_id: int
    test_id: int
    student_answer: str
    is_correct: int
    created_at: datetime

    class Config:
        from_attributes = True


# Weak Topic Report Schemas
class WeakTopicReportResponse(BaseModel):
    id: int
    student_id: int
    test_id: int
    topic: str
    score: float
    total_questions: int
    correct_answers: int
    is_weak: int
    recommendation: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TestAnalysisResponse(BaseModel):
    test_id: int
    overall_score: float
    total_questions: int
    correct_answers: int
    weak_topics: List[WeakTopicReportResponse]
    score_breakdown: dict  # {topic: score}
    recommendation_message: str


# GDPI Schemas
class GDPIQuestionResponse(BaseModel):
    id: int
    question_text: str
    category: str
    difficulty: str

    class Config:
        from_attributes = True


class GDPIResponseCreate(BaseModel):
    question_id: int
    response_text: str


class GDPIResponseSubmit(BaseModel):
    responses: List[GDPIResponseCreate]


class GDPIResponseResponse(BaseModel):
    id: int
    student_id: int
    question_id: int
    response_text: str
    score: float
    feedback: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


# Placement Profile Schemas
class PlacementProfileCreate(BaseModel):
    skills: List[str]
    projects: Optional[List[str]] = None
    cgpa: float
    experience: Optional[str] = None


class PlacementProfileUpdate(BaseModel):
    skills: Optional[List[str]] = None
    projects: Optional[List[str]] = None
    cgpa: Optional[float] = None
    experience: Optional[str] = None


class PlacementProfileResponse(BaseModel):
    id: int
    student_id: int
    skills: List[str]
    projects: Optional[List[str]] = None
    cgpa: float
    experience: Optional[str] = None
    best_fit_domain: Optional[str] = None
    domain_scores: dict
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Certificate Schemas
class CertificateCreate(BaseModel):
    course_name: str
    organization: str
    issued_date: str  # YYYY-MM-DD
    expiry_date: Optional[str] = None
    certificate_url: Optional[str] = None
    notes: Optional[str] = None


class CertificateResponse(BaseModel):
    id: int
    student_id: int
    course_name: str
    organization: str
    issued_date: str
    expiry_date: Optional[str] = None
    certificate_url: Optional[str] = None
    verification_status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# JWT Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class TokenPayload(BaseModel):
    sub: int
    exp: int
