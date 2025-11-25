# AIOS Backend - API Testing Guide

This guide provides examples for testing all API endpoints using curl commands.

## Prerequisites

- AIOS Backend running at `http://localhost:8000`
- Database seeded with sample data
- JWT token from login (stored as `$TOKEN`)

## Quick Commands

### Set Token Variable (macOS/Linux)
```bash
TOKEN="your-jwt-token-here"
```

### Set Token Variable (Windows PowerShell)
```powershell
$token = "your-jwt-token-here"
```

---

## 1. Authentication Endpoints

### Register New User
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "email": "jane@example.com",
    "password": "securepass123",
    "role": "student"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "amit@student.aios.edu",
    "password": "student123"
  }'
```

**Save the token from response:**
```bash
TOKEN="<access_token_from_response>"
```

### Get Current User Info
```bash
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

### Get User by ID
```bash
curl -X GET "http://localhost:8000/api/auth/users/1" \
  -H "Authorization: Bearer $TOKEN"
```

### List All Users (Admin Only)
```bash
curl -X GET "http://localhost:8000/api/auth/admin/users" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 2. Test & Analysis Endpoints

### List All Tests
```bash
curl -X GET "http://localhost:8000/api/tests/" \
  -H "Authorization: Bearer $TOKEN"
```

### Get Test Details
```bash
curl -X GET "http://localhost:8000/api/tests/1" \
  -H "Authorization: Bearer $TOKEN"
```

### Create New Test (Faculty Only)
```bash
curl -X POST "http://localhost:8000/api/tests/create" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Programming Quiz",
    "description": "Test on Python fundamentals",
    "questions": [
      {
        "question_text": "What is the output of print(2 ** 3)?",
        "topic": "Programming",
        "correct_answer": "8",
        "options": "[\"6\", \"8\", \"9\", \"12\"]",
        "difficulty": "easy"
      },
      {
        "question_text": "What does len() function do?",
        "topic": "Built-in Functions",
        "correct_answer": "Returns the length of an object",
        "difficulty": "easy"
      }
    ]
  }'
```

### Submit Test Answers
```bash
curl -X POST "http://localhost:8000/api/tests/submit-answers" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "test_id": 1,
    "answers": [
      {
        "question_id": 1,
        "student_answer": "O(log n)"
      },
      {
        "question_id": 2,
        "student_answer": "Stack"
      },
      {
        "question_id": 3,
        "student_answer": "O(n log n)"
      },
      {
        "question_id": 4,
        "student_answer": "It describes upper bound of algorithm complexity"
      }
    ]
  }'
```

Response includes:
- Overall score
- Total questions and correct answers
- Weak topics (score < 70%)
- Score breakdown by topic
- Personalized recommendation message

### Get Test Analysis
```bash
curl -X GET "http://localhost:8000/api/tests/analysis/1" \
  -H "Authorization: Bearer $TOKEN"
```

### Faculty - Get Class Weak Topics
```bash
curl -X GET "http://localhost:8000/api/tests/faculty/weak-topics" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 3. GDPI (Mock Interview) Endpoints

### Fetch GDPI Questions
```bash
curl -X GET "http://localhost:8000/api/gdpi/questions?limit=5" \
  -H "Authorization: Bearer $TOKEN"
```

### Fetch GDPI Questions by Category
```bash
# Categories: technical, hr, behavioral
curl -X GET "http://localhost:8000/api/gdpi/questions?category=technical&limit=3" \
  -H "Authorization: Bearer $TOKEN"
```

### Submit GDPI Responses
```bash
curl -X POST "http://localhost:8000/api/gdpi/submit" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "responses": [
      {
        "question_id": 1,
        "response_text": "I am Amit Patel, a passionate software developer with expertise in data structures and algorithms. I have 2 years of internship experience where I worked on scalable backend systems. My career goal is to join a top tech company and work on challenging problems that impact millions of users."
      },
      {
        "question_id": 2,
        "response_text": "Object-Oriented Programming is a paradigm based on encapsulation, inheritance, and polymorphism. Encapsulation helps bundle data and methods together. Inheritance allows code reuse through classes. Polymorphism enables objects to take multiple forms."
      }
    ]
  }'
```

Response includes:
- Total responses evaluated
- Average score (0-10)
- Individual response scores and feedback

### Get Student GDPI Responses
```bash
curl -X GET "http://localhost:8000/api/gdpi/student-responses" \
  -H "Authorization: Bearer $TOKEN"
```

### Get Specific Response
```bash
curl -X GET "http://localhost:8000/api/gdpi/responses/1" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 4. Placement Segregation Endpoints

### Analyze Skills (Without Saving)
```bash
curl -X POST "http://localhost:8000/api/placement/analyze" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skills": ["React", "Node.js", "JavaScript", "CSS", "MongoDB"],
    "projects": ["E-commerce Platform", "Social Media API"],
    "cgpa": 3.7,
    "experience": "1 year internship"
  }'
```

Response shows:
- Best-fit domain (e.g., "Web")
- Domain scores for all categories

### Create/Update Placement Profile
```bash
curl -X POST "http://localhost:8000/api/placement/profile" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skills": ["Python", "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning", "Data Science"],
    "projects": ["Image Classification Model", "NLP Chatbot"],
    "cgpa": 3.9,
    "experience": "Kaggle competitions"
  }'
```

### Get My Placement Profile
```bash
curl -X GET "http://localhost:8000/api/placement/profile" \
  -H "Authorization: Bearer $TOKEN"
```

### Get Students by Domain
```bash
# Domains: Web, ML, Cloud, Cybersecurity, Generalist
curl -X GET "http://localhost:8000/api/placement/domain/Web" \
  -H "Authorization: Bearer $TOKEN"
```

### Get Top Students in Domain
```bash
curl -X GET "http://localhost:8000/api/placement/domain/ML/top?limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 5. Certificate Management Endpoints

### Upload Certificate
```bash
curl -X POST "http://localhost:8000/api/certificates/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "course_name": "AWS Solutions Architect Associate",
    "organization": "Amazon Web Services",
    "issued_date": "2023-06-15",
    "expiry_date": "2026-06-15",
    "certificate_url": "https://example.com/cert/aws123",
    "notes": "Professional certification - passing score 720/1000"
  }'
```

### Get My Certificates
```bash
curl -X GET "http://localhost:8000/api/certificates/my-certificates" \
  -H "Authorization: Bearer $TOKEN"
```

### Get My Verified Certificates
```bash
curl -X GET "http://localhost:8000/api/certificates/my-verified" \
  -H "Authorization: Bearer $TOKEN"
```

### Get Certificate Details
```bash
curl -X GET "http://localhost:8000/api/certificates/1" \
  -H "Authorization: Bearer $TOKEN"
```

### Verify Certificate (Admin Only)
```bash
curl -X POST "http://localhost:8000/api/certificates/verify/1" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d 'status=verified&notes=Verified+against+official+records'
```

Or with query parameters:
```bash
curl -X POST "http://localhost:8000/api/certificates/verify/1?status_update=verified&notes=Verified" \
  -H "Authorization: Bearer $TOKEN"
```

### Get Pending Certificates (Admin Only)
```bash
curl -X GET "http://localhost:8000/api/certificates/admin/pending" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Test Scenarios

### Complete Student Flow

1. **Register**
```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Student","email":"test@student.edu","password":"pass123","role":"student"}'
```

2. **Login**
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@student.edu","password":"pass123"}'
```

3. **Get Tests**
```bash
TOKEN="<from_login_response>"
curl -X GET "http://localhost:8000/api/tests/" \
  -H "Authorization: Bearer $TOKEN"
```

4. **Submit Answers**
```bash
curl -X POST "http://localhost:8000/api/tests/submit-answers" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"test_id":1,"answers":[{"question_id":1,"student_answer":"correct_answer"}]}'
```

5. **Create Placement Profile**
```bash
curl -X POST "http://localhost:8000/api/placement/profile" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"skills":["Skill1","Skill2"],"cgpa":3.5}'
```

6. **Submit GDPI Responses**
```bash
curl -X POST "http://localhost:8000/api/gdpi/submit" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"responses":[{"question_id":1,"response_text":"detailed response"}]}'
```

7. **Upload Certificate**
```bash
curl -X POST "http://localhost:8000/api/certificates/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"course_name":"Course","organization":"Org","issued_date":"2023-01-01"}'
```

---

## Sample Credentials

```
Admin User:
  Email: admin@aios.edu
  Password: admin123

Faculty User:
  Email: rajesh@aios.edu
  Password: faculty123

Student User:
  Email: amit@student.aios.edu
  Password: student123
```

---

## Health Check

```bash
curl -X GET "http://localhost:8000/health"
```

---

## API Documentation

Interactive documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## Error Examples

### Missing Token
```bash
curl -X GET "http://localhost:8000/api/auth/me"
# Response: 403 Forbidden - Missing authentication token
```

### Invalid Email
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"invalid","password":"pass"}'
# Response: 422 Unprocessable Entity - Invalid email format
```

### Weak Topic Example Response
```json
{
  "test_id": 1,
  "overall_score": 75.0,
  "total_questions": 4,
  "correct_answers": 3,
  "weak_topics": [
    {
      "id": 1,
      "student_id": 2,
      "test_id": 1,
      "topic": "Algorithms",
      "score": 50.0,
      "total_questions": 2,
      "correct_answers": 1,
      "is_weak": 1,
      "recommendation": "Weak: Algorithms needs improvement. Dedicate extra time to practice."
    }
  ],
  "score_breakdown": {
    "Data Structures": 100.0,
    "Algorithms": 50.0
  },
  "recommendation_message": "Good effort! Review the weak topics and practice more to improve."
}
```

### Placement Profile Example Response
```json
{
  "id": 1,
  "student_id": 2,
  "skills": ["React", "Node.js", "JavaScript", "CSS", "HTML"],
  "projects": ["E-commerce", "Blog"],
  "cgpa": 3.8,
  "experience": "1 year",
  "best_fit_domain": "Web",
  "domain_scores": {
    "Web": 80.0,
    "ML": 10.0,
    "Cloud": 20.0,
    "Cybersecurity": 5.0
  }
}
```

---

## Tips

1. **Always include `Authorization` header** for authenticated endpoints
2. **Content-Type**: Use `application/json` for POST requests
3. **URL Encoding**: Use `%20` for spaces in query parameters
4. **Token Expiry**: Tokens expire after 30 minutes, re-login to get new one
5. **Date Format**: Use `YYYY-MM-DD` for date fields
6. **JSON**: Ensure all JSON is properly formatted

---

**Last Updated**: November 2025
