"""
Seed data script for AIOS Backend
Creates sample data for testing and development
"""

import json
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine
from app.models import Base
from app.models.user import User, UserRole
from app.models.test import Test, Question
from app.models.gdpi import GDPIQuestion
from app.core.security import hash_password


def create_admin_user(db: Session):
    """Create admin user"""
    admin = User(
        name="Admin User",
        email="admin@aios.edu",
        password_hash=hash_password("admin123"),
        role=UserRole.ADMIN,
        bio="System administrator",
    )
    db.add(admin)
    db.commit()
    return admin


def create_faculty_users(db: Session):
    """Create faculty users"""
    faculty_users = [
        User(
            name="Dr. Rajesh Kumar",
            email="rajesh@aios.edu",
            password_hash=hash_password("faculty123"),
            role=UserRole.FACULTY,
            bio="Computer Science faculty",
        ),
        User(
            name="Dr. Priya Sharma",
            email="priya@aios.edu",
            password_hash=hash_password("faculty123"),
            role=UserRole.FACULTY,
            bio="Data Science faculty",
        ),
    ]
    for faculty in faculty_users:
        db.add(faculty)
    db.commit()
    return faculty_users


def create_student_users(db: Session):
    """Create student users"""
    students = [
        User(
            name="Amit Patel",
            email="amit@student.aios.edu",
            password_hash=hash_password("student123"),
            role=UserRole.STUDENT,
            bio="CSE Student",
        ),
        User(
            name="Sana Khan",
            email="sana@student.aios.edu",
            password_hash=hash_password("student123"),
            role=UserRole.STUDENT,
            bio="Data Science Enthusiast",
        ),
        User(
            name="Rohan Singh",
            email="rohan@student.aios.edu",
            password_hash=hash_password("student123"),
            role=UserRole.STUDENT,
            bio="Web Development Student",
        ),
    ]
    for student in students:
        db.add(student)
    db.commit()
    return students


def create_tests(db: Session, faculty_user):
    """Create test papers"""
    test1 = Test(
        title="Data Structures Midterm",
        description="Test on arrays, linked lists, and trees",
        created_by=faculty_user.id,
    )
    db.add(test1)
    db.flush()
    
    # Add questions for test1
    questions_data = [
        {
            "question_text": "What is the time complexity of binary search?",
            "topic": "Data Structures",
            "correct_answer": "O(log n)",
            "options": json.dumps(["O(n)", "O(log n)", "O(n^2)", "O(1)"]),
            "difficulty": "medium",
        },
        {
            "question_text": "Which data structure uses LIFO?",
            "topic": "Data Structures",
            "correct_answer": "Stack",
            "options": json.dumps(["Stack", "Queue", "Tree", "Graph"]),
            "difficulty": "easy",
        },
        {
            "question_text": "What is the average case time complexity of quicksort?",
            "topic": "Algorithms",
            "correct_answer": "O(n log n)",
            "options": json.dumps(["O(n)", "O(n log n)", "O(n^2)", "O(log n)"]),
            "difficulty": "medium",
        },
        {
            "question_text": "Define Big O notation",
            "topic": "Algorithms",
            "correct_answer": "It describes upper bound of algorithm complexity",
            "options": None,
            "difficulty": "hard",
        },
    ]
    
    for q_data in questions_data:
        question = Question(
            test_id=test1.id,
            question_text=q_data["question_text"],
            topic=q_data["topic"],
            correct_answer=q_data["correct_answer"],
            options=q_data["options"],
            difficulty=q_data["difficulty"],
        )
        db.add(question)
    
    db.commit()
    return test1


def create_gdpi_questions(db: Session):
    """Create GDPI interview questions"""
    questions = [
        GDPIQuestion(
            question_text="Tell me about yourself and your career goals.",
            category="hr",
            difficulty="easy",
            keywords=json.dumps(["skills", "experience", "career", "goals", "passion"]),
        ),
        GDPIQuestion(
            question_text="What is your understanding of Object-Oriented Programming?",
            category="technical",
            difficulty="medium",
            keywords=json.dumps(["encapsulation", "inheritance", "polymorphism", "classes", "objects"]),
        ),
        GDPIQuestion(
            question_text="Describe a challenging project you have worked on.",
            category="behavioral",
            difficulty="medium",
            keywords=json.dumps(["problem", "solution", "teamwork", "leadership", "achievement"]),
        ),
        GDPIQuestion(
            question_text="What is the difference between SQL and NoSQL databases?",
            category="technical",
            difficulty="hard",
            keywords=json.dumps(["relational", "schema", "scalability", "ACID", "flexibility"]),
        ),
        GDPIQuestion(
            question_text="How do you handle failure and learn from mistakes?",
            category="behavioral",
            difficulty="medium",
            keywords=json.dumps(["reflection", "improvement", "resilience", "learning", "growth"]),
        ),
    ]
    
    for question in questions:
        db.add(question)
    
    db.commit()
    return questions


def seed_database():
    """Main function to seed database with sample data"""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Create users
        print("Creating admin user...")
        admin = create_admin_user(db)
        print(f"✓ Admin created: {admin.email}")
        
        print("Creating faculty users...")
        faculty_users = create_faculty_users(db)
        print(f"✓ {len(faculty_users)} faculty created")
        
        print("Creating student users...")
        student_users = create_student_users(db)
        print(f"✓ {len(student_users)} students created")
        
        print("Creating test papers...")
        test = create_tests(db, faculty_users[0])
        print(f"✓ Test created: {test.title}")
        
        print("Creating GDPI questions...")
        gdpi_questions = create_gdpi_questions(db)
        print(f"✓ {len(gdpi_questions)} GDPI questions created")
        
        print("\n✅ Database seeding completed successfully!")
        print("\nSample credentials for testing:")
        print(f"  Admin: admin@aios.edu / admin123")
        print(f"  Faculty: rajesh@aios.edu / faculty123")
        print(f"  Student: amit@student.aios.edu / student123")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
