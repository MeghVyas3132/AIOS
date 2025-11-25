from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json
from app.core.database import get_db
from app.core.deps import get_current_user, require_faculty, require_student
from app.models.user import User
from app.models.test import Test, Question, Answer
from app.schemas import (
    TestCreate, TestResponse, QuestionCreate, StudentTestAnswerCreate,
    AnswerCreate, TestAnalysisResponse, WeakTopicReportResponse
)
from app.services.weak_topic_service import get_test_analysis, get_faculty_weak_topics

router = APIRouter(prefix="/api/tests", tags=["Tests & Analysis"])


@router.post("/create", response_model=TestResponse)
async def create_test(
    test_data: TestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_faculty),
):
    """
    Create a new test (faculty only)
    """
    # Create test
    test = Test(
        title=test_data.title,
        description=test_data.description,
        created_by=current_user.id,
    )
    db.add(test)
    db.flush()  # To get test.id
    
    # Create questions
    if test_data.questions:
        for q_data in test_data.questions:
            question = Question(
                test_id=test.id,
                question_text=q_data.question_text,
                topic=q_data.topic,
                correct_answer=q_data.correct_answer,
                options=q_data.options,
                difficulty=q_data.difficulty,
            )
            db.add(question)
    
    db.commit()
    db.refresh(test)
    return test


@router.get("/{test_id}", response_model=TestResponse)
async def get_test(
    test_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get test details by ID"""
    test = db.query(Test).filter(Test.id == test_id).first()
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found",
        )
    return test


@router.get("/", response_model=List[TestResponse])
async def list_tests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List all available tests"""
    tests = db.query(Test).all()
    return tests


@router.post("/submit-answers", response_model=TestAnalysisResponse)
async def submit_test_answers(
    submission: StudentTestAnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
):
    """
    Submit test answers and get analysis
    Analyzes answers and identifies weak topics
    """
    # Verify test exists
    test = db.query(Test).filter(Test.id == submission.test_id).first()
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found",
        )
    
    # Create answer records
    for answer_data in submission.answers:
        # Verify question exists and belongs to test
        question = db.query(Question).filter(
            Question.id == answer_data.question_id,
            Question.test_id == submission.test_id,
        ).first()
        
        if not question:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Question {answer_data.question_id} not found in this test",
            )
        
        # Create answer record
        answer = Answer(
            question_id=answer_data.question_id,
            student_id=current_user.id,
            test_id=submission.test_id,
            student_answer=answer_data.student_answer,
        )
        db.add(answer)
    
    db.commit()
    
    # Analyze test performance
    analysis = get_test_analysis(db, current_user.id, submission.test_id)
    
    return {
        "test_id": analysis["test_id"],
        "overall_score": analysis["overall_score"],
        "total_questions": analysis["total_questions"],
        "correct_answers": analysis["correct_answers"],
        "weak_topics": analysis["weak_topics"],
        "score_breakdown": analysis["score_breakdown"],
        "recommendation_message": analysis["recommendation_message"],
    }


@router.get("/analysis/{test_id}", response_model=TestAnalysisResponse)
async def get_test_analysis_endpoint(
    test_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
):
    """Get analysis for a specific test (student's own results)"""
    # Verify test exists
    test = db.query(Test).filter(Test.id == test_id).first()
    if not test:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test not found",
        )
    
    # Get analysis
    analysis = get_test_analysis(db, current_user.id, test_id)
    
    return {
        "test_id": analysis["test_id"],
        "overall_score": analysis["overall_score"],
        "total_questions": analysis["total_questions"],
        "correct_answers": analysis["correct_answers"],
        "weak_topics": analysis["weak_topics"],
        "score_breakdown": analysis["score_breakdown"],
        "recommendation_message": analysis["recommendation_message"],
    }


@router.get("/faculty/weak-topics", response_model=List[WeakTopicReportResponse])
async def faculty_weak_topics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_faculty),
):
    """
    Get weak topics for all students who took the faculty's tests
    Faculty only endpoint
    """
    weak_topics = get_faculty_weak_topics(db, current_user.id)
    return weak_topics
