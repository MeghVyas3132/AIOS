from sqlalchemy.orm import Session
from typing import List, Dict
import json
from app.models.test import Test, Question, Answer
from app.models.weak_topic import WeakTopicReport
from app.core.config import WEAK_TOPIC_THRESHOLD


def compare_answers(db: Session, student_id: int, test_id: int) -> Dict:
    """
    Compare student answers with correct answers and calculate scores per topic
    Returns score breakdown and weak topics
    """
    # Get all questions in the test
    questions = db.query(Question).filter(Question.test_id == test_id).all()
    
    # Get all student answers for this test
    answers = db.query(Answer).filter(
        Answer.student_id == student_id,
        Answer.test_id == test_id
    ).all()
    
    # Create a mapping of question_id to answer
    answer_map = {answer.question_id: answer for answer in answers}
    
    # Calculate scores per topic
    topic_scores = {}
    for question in questions:
        if question.id not in answer_map:
            continue
        
        answer = answer_map[question.id]
        topic = question.topic
        
        if topic not in topic_scores:
            topic_scores[topic] = {
                "total": 0,
                "correct": 0,
                "questions": []
            }
        
        topic_scores[topic]["total"] += 1
        topic_scores[topic]["questions"].append(question.id)
        
        # Simple comparison (case-insensitive, trimmed)
        is_correct = (
            answer.student_answer.strip().lower() == 
            question.correct_answer.strip().lower()
        )
        
        if is_correct:
            topic_scores[topic]["correct"] += 1
            answer.is_correct = 1
        else:
            answer.is_correct = 0
        
        db.add(answer)
    
    db.commit()
    
    return topic_scores


def calculate_score_breakdown(topic_scores: Dict) -> Dict:
    """Calculate percentage scores for each topic"""
    breakdown = {}
    for topic, data in topic_scores.items():
        if data["total"] > 0:
            percentage = (data["correct"] / data["total"]) * 100
            breakdown[topic] = round(percentage, 2)
    return breakdown


def identify_weak_topics(
    db: Session,
    student_id: int,
    test_id: int,
    topic_scores: Dict,
    threshold: float = WEAK_TOPIC_THRESHOLD,
) -> List[WeakTopicReport]:
    """Identify topics where score is below threshold"""
    weak_topics = []
    
    for topic, data in topic_scores.items():
        if data["total"] == 0:
            continue
        
        score_percentage = (data["correct"] / data["total"]) * 100
        is_weak = 1 if score_percentage < threshold else 0
        
        # Generate recommendation
        recommendation = generate_recommendation(topic, score_percentage)
        
        # Create weak topic report
        report = WeakTopicReport(
            student_id=student_id,
            test_id=test_id,
            topic=topic,
            score=round(score_percentage, 2),
            total_questions=data["total"],
            correct_answers=data["correct"],
            is_weak=is_weak,
            threshold=threshold,
            recommendation=recommendation,
        )
        db.add(report)
        weak_topics.append(report)
    
    db.commit()
    
    # Filter only weak topics
    return [t for t in weak_topics if t.is_weak == 1]


def generate_recommendation(topic: str, score: float) -> str:
    """Generate personalized recommendation based on score"""
    if score < 30:
        return f"Critical: Focus on {topic}. Review fundamentals and practice more problems."
    elif score < 50:
        return f"Weak: {topic} needs improvement. Dedicate extra time to practice."
    elif score < 70:
        return f"Below Average: {topic} requires more practice and revision."
    else:
        return f"Good: Keep practicing {topic} to maintain and improve."


def get_test_analysis(
    db: Session,
    student_id: int,
    test_id: int,
) -> Dict:
    """Get comprehensive test analysis for a student"""
    # Compare answers and get topic scores
    topic_scores = compare_answers(db, student_id, test_id)
    
    # Calculate score breakdown
    score_breakdown = calculate_score_breakdown(topic_scores)
    
    # Identify weak topics
    weak_topics_list = identify_weak_topics(db, student_id, test_id, topic_scores)
    
    # Calculate overall score
    total_questions = sum(data["total"] for data in topic_scores.values())
    correct_answers = sum(data["correct"] for data in topic_scores.values())
    overall_score = (
        (correct_answers / total_questions) * 100 
        if total_questions > 0 else 0
    )
    
    # Generate overall recommendation
    if overall_score < 50:
        recommendation_message = "You need significant improvement. Focus on weak topics and practice regularly."
    elif overall_score < 70:
        recommendation_message = "Good effort! Review the weak topics and practice more to improve."
    elif overall_score < 85:
        recommendation_message = "Great performance! Continue with consistent practice to reach excellence."
    else:
        recommendation_message = "Excellent! You have mastered the content. Help peers and take advanced topics."
    
    return {
        "test_id": test_id,
        "overall_score": round(overall_score, 2),
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "weak_topics": weak_topics_list,
        "score_breakdown": score_breakdown,
        "recommendation_message": recommendation_message,
    }


def get_faculty_weak_topics(db: Session, faculty_id: int):
    """Get weak topics for all students of a faculty's tests"""
    # Get all tests created by faculty
    tests = db.query(Test).filter(Test.created_by == faculty_id).all()
    test_ids = [t.id for t in tests]
    
    if not test_ids:
        return []
    
    # Get all weak topic reports for these tests
    weak_topics = db.query(WeakTopicReport).filter(
        WeakTopicReport.test_id.in_(test_ids),
        WeakTopicReport.is_weak == 1
    ).all()
    
    return weak_topics
