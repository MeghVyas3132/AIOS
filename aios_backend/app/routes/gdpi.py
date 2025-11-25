from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json
from app.core.database import get_db
from app.core.deps import get_current_user, require_student
from app.models.user import User
from app.models.gdpi import GDPIQuestion, GDPIResponse
from app.schemas import GDPIQuestionResponse, GDPIResponseSubmit, GDPIResponseResponse
from app.services.gdpi_service import (
    get_gdpi_questions, get_gdpi_questions_by_category,
    submit_gdpi_response, get_student_gdpi_responses
)

router = APIRouter(prefix="/api/gdpi", tags=["GDPI"])


@router.get("/questions", response_model=List[GDPIQuestionResponse])
async def fetch_gdpi_questions(
    category: str = None,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Fetch curated GDPI interview questions
    Optional filter by category: technical, hr, behavioral
    """
    if category:
        questions = get_gdpi_questions_by_category(db, category, limit)
    else:
        questions = get_gdpi_questions(db, limit)
    
    return questions


@router.post("/submit", response_model=dict)
async def submit_gdpi_responses(
    submission: GDPIResponseSubmit,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
):
    """
    Submit GDPI responses
    Each response is evaluated with rule-based logic (keyword matching)
    """
    responses = []
    total_score = 0
    
    for response_data in submission.responses:
        try:
            gdpi_response = submit_gdpi_response(
                db,
                student_id=current_user.id,
                question_id=response_data.question_id,
                response_text=response_data.response_text,
            )
            responses.append(gdpi_response)
            total_score += gdpi_response.score
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )
    
    average_score = total_score / len(responses) if responses else 0
    
    return {
        "message": "Responses submitted and evaluated successfully",
        "total_responses": len(responses),
        "average_score": round(average_score, 2),
        "responses": responses,
    }


@router.get("/student-responses", response_model=dict)
async def get_student_responses(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
):
    """Get all GDPI responses for the current student"""
    result = get_student_gdpi_responses(db, current_user.id)
    return result


@router.get("/responses/{response_id}", response_model=GDPIResponseResponse)
async def get_response_details(
    response_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student),
):
    """Get details of a specific GDPI response"""
    response = db.query(GDPIResponse).filter(
        GDPIResponse.id == response_id,
        GDPIResponse.student_id == current_user.id,
    ).first()
    
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Response not found",
        )
    
    return response
