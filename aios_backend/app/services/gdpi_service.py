from sqlalchemy.orm import Session
from typing import List, Dict
import json
from app.models.gdpi import GDPIQuestion, GDPIResponse


def get_gdpi_questions(db: Session, limit: int = 10) -> List[GDPIQuestion]:
    """Fetch curated GDPI questions"""
    return db.query(GDPIQuestion).limit(limit).all()


def get_gdpi_questions_by_category(
    db: Session,
    category: str,
    limit: int = 5,
) -> List[GDPIQuestion]:
    """Fetch GDPI questions by category"""
    return db.query(GDPIQuestion).filter(
        GDPIQuestion.category == category
    ).limit(limit).all()


def evaluate_gdpi_response(response_text: str, keywords: List[str]) -> tuple:
    """
    Rule-based evaluation of GDPI response
    Returns: (score, matched_keywords)
    """
    response_lower = response_text.lower()
    matched_keywords = []
    
    # Count matched keywords
    for keyword in keywords:
        if keyword.lower() in response_lower:
            matched_keywords.append(keyword)
    
    # Calculate score based on keyword matches (0-10 scale)
    if not keywords:
        score = 5.0  # Neutral score if no keywords defined
    else:
        keyword_match_percentage = len(matched_keywords) / len(keywords)
        score = keyword_match_percentage * 10
    
    # Bonus for response length (shows effort and detail)
    word_count = len(response_text.split())
    if word_count >= 50:
        score = min(score + 1, 10)  # Add bonus but cap at 10
    
    return round(score, 2), matched_keywords


def submit_gdpi_response(
    db: Session,
    student_id: int,
    question_id: int,
    response_text: str,
) -> GDPIResponse:
    """Submit and evaluate a GDPI response"""
    # Get the question
    question = db.query(GDPIQuestion).filter(
        GDPIQuestion.id == question_id
    ).first()
    
    if not question:
        raise ValueError(f"Question {question_id} not found")
    
    # Parse keywords from JSON
    keywords = json.loads(question.keywords) if isinstance(question.keywords, str) else question.keywords
    
    # Evaluate response
    score, matched_keywords = evaluate_gdpi_response(response_text, keywords)
    
    # Generate feedback
    feedback = generate_gdpi_feedback(score, matched_keywords, keywords)
    
    # Create response record
    gdpi_response = GDPIResponse(
        student_id=student_id,
        question_id=question_id,
        response_text=response_text,
        score=score,
        keywords_matched=json.dumps(matched_keywords),
        feedback=feedback,
    )
    
    db.add(gdpi_response)
    db.commit()
    db.refresh(gdpi_response)
    
    return gdpi_response


def generate_gdpi_feedback(
    score: float,
    matched_keywords: List[str],
    all_keywords: List[str],
) -> str:
    """Generate feedback for GDPI response"""
    if score >= 8:
        feedback = "Excellent response! You covered key points comprehensively."
    elif score >= 6:
        feedback = f"Good response! You mentioned {len(matched_keywords)} relevant points. Try to include more details."
    elif score >= 4:
        feedback = f"Fair response. You covered {len(matched_keywords)} out of {len(all_keywords)} key points. Improve your coverage."
    else:
        feedback = "Needs improvement. Focus on key concepts and provide more detailed answers."
    
    return feedback


def get_student_gdpi_responses(
    db: Session,
    student_id: int,
) -> Dict:
    """Get all GDPI responses for a student with average score"""
    responses = db.query(GDPIResponse).filter(
        GDPIResponse.student_id == student_id
    ).all()
    
    if not responses:
        return {
            "total_responses": 0,
            "average_score": 0,
            "responses": [],
        }
    
    average_score = sum(r.score for r in responses) / len(responses)
    
    return {
        "total_responses": len(responses),
        "average_score": round(average_score, 2),
        "responses": responses,
    }
