# AIOS Backend - College AI Ecosystem MVP

A comprehensive FastAPI backend for a college AI ecosystem management system. This MVP uses rule-based logic (no AI) to provide modules for user authentication, test analysis, GDPI interviews, placement segregation, and certificate management.

## Features

### 1. **User Authentication**
- JWT-based authentication
- Role-based access control (Student, Faculty, Admin)
- Secure password hashing with bcrypt
- User registration and login endpoints

### 2. **Weak Topic Analyzer (Rule-Based)**
- Analyze student test answers
- Calculate scores per topic
- Identify weak topics (below threshold)
- Generate personalized recommendations
- Faculty endpoint to view class weak topics

### 3. **GDPI Module (Mock Interview)**
- Curated interview questions by category (technical, HR, behavioral)
- Rule-based response evaluation using keyword matching
- Score generation (0-10 scale)
- Feedback generation based on performance
- Student response history tracking

### 4. **Placement Segregation (Rule-Based)**
- Skill-based domain matching
- Domain categories: Web, ML, Cloud, Cybersecurity
- Rule-based skill matching algorithm
- CGPA tracking for ranking
- Best-fit domain recommendation

### 5. **Certificate Management**
- Certificate metadata upload
- Validation of certificate fields
- Verification status tracking (pending, verified, rejected)
- Admin verification endpoints

## Technology Stack

- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT with PyJWT
- **Password Hashing**: Passlib + bcrypt
- **API Server**: Uvicorn
- **Validation**: Pydantic

## Project Structure

```
aios_backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py           # Configuration settings
│   │   ├── database.py         # Database connection and session
│   │   ├── security.py         # JWT and password utilities
│   │   └── deps.py             # Dependency injection for auth
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py             # SQLAlchemy Base
│   │   ├── user.py             # User model
│   │   ├── test.py             # Test, Question, Answer models
│   │   ├── weak_topic.py       # WeakTopicReport model
│   │   ├── gdpi.py             # GDPI models
│   │   ├── placement.py        # PlacementProfile model
│   │   └── certificate.py      # Certificate model
│   ├── schemas/
│   │   └── __init__.py         # Pydantic schemas for all models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py     # Authentication logic
│   │   ├── weak_topic_service.py # Test analysis logic
│   │   ├── gdpi_service.py     # GDPI evaluation logic
│   │   ├── placement_service.py # Placement analysis logic
│   │   └── certificate_service.py # Certificate validation logic
│   └── routes/
│       ├── __init__.py
│       ├── auth.py             # Authentication endpoints
│       ├── tests.py            # Test and analysis endpoints
│       ├── gdpi.py             # GDPI endpoints
│       ├── placement.py        # Placement endpoints
│       └── certificates.py     # Certificate endpoints
├── seed_data.py                # Database seeding script
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables example
└── README.md                  # This file
```

## Database Models

### Users
- id, name, email, password_hash, role, bio, created_at, updated_at

### Tests
- id, title, description, created_by (faculty), created_at, updated_at

### Questions
- id, test_id, question_text, topic, correct_answer, options, difficulty, created_at

### Answers
- id, question_id, student_id, test_id, student_answer, is_correct, created_at

### WeakTopicReports
- id, student_id, test_id, topic, score, total_questions, correct_answers, is_weak, threshold, recommendation, created_at

### GDPIQuestions
- id, question_text, category, difficulty, keywords (JSON), created_at

### GDPIResponses
- id, student_id, question_id, response_text, score, keywords_matched (JSON), feedback, created_at

### PlacementProfiles
- id, student_id, skills (JSON), projects (JSON), cgpa, experience, best_fit_domain, domain_scores (JSON), created_at, updated_at

### Certificates
- id, student_id, course_name, organization, issued_date, expiry_date, certificate_url, verification_status, notes, created_at, updated_at

## Setup Instructions

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- pip (Python package manager)

### Installation

1. **Clone the repository and navigate to the backend directory**
   ```bash
   cd aios_backend
   ```

2. **Create a Python virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` with your configuration:
   ```env
   DATABASE_URL=postgresql://aios_user:aios_password@localhost:5432/aios_db
   JWT_SECRET=your-secret-key-change-in-production
   ```

5. **Set up PostgreSQL database**
   ```bash
   # Create database and user (run in PostgreSQL)
   psql -U postgres
   
   CREATE USER aios_user WITH PASSWORD 'aios_password';
   CREATE DATABASE aios_db OWNER aios_user;
   GRANT ALL PRIVILEGES ON DATABASE aios_db TO aios_user;
   \q
   ```

6. **Seed the database with sample data**
   ```bash
   python seed_data.py
   ```
   
   This will create:
   - 1 admin user
   - 2 faculty users
   - 3 student users
   - Sample test with questions
   - GDPI interview questions

## Running the Application

### Development Mode with Auto-Reload

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at `http://localhost:8000`

### Interactive API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication (`/api/auth`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/register` | Register new user | Public |
| POST | `/login` | Login and get JWT token | Public |
| GET | `/me` | Get current user info | Authenticated |
| GET | `/users/{user_id}` | Get user by ID | Authenticated |
| GET | `/admin/users` | List all users | Admin only |

### Tests & Analysis (`/api/tests`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/create` | Create new test | Faculty only |
| GET | `/{test_id}` | Get test details | Authenticated |
| GET | `/` | List all tests | Authenticated |
| POST | `/submit-answers` | Submit test answers | Student only |
| GET | `/analysis/{test_id}` | Get test analysis | Student only |
| GET | `/faculty/weak-topics` | Faculty's class weak topics | Faculty only |

### GDPI (`/api/gdpi`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/questions` | Fetch GDPI questions | Authenticated |
| GET | `/questions?category=technical` | Fetch by category | Authenticated |
| POST | `/submit` | Submit responses | Student only |
| GET | `/student-responses` | Get my responses | Student only |
| GET | `/responses/{response_id}` | Get response details | Student only |

### Placement (`/api/placement`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/profile` | Create/update profile | Student only |
| GET | `/profile` | Get my profile | Student only |
| POST | `/analyze` | Analyze without saving | Student only |
| GET | `/domain/{domain}` | Get students by domain | Authenticated |
| GET | `/domain/{domain}/top` | Get top students | Authenticated |

### Certificates (`/api/certificates`)

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/upload` | Upload certificate | Student only |
| GET | `/my-certificates` | Get my certificates | Student only |
| GET | `/my-verified` | Get verified certs | Student only |
| GET | `/{certificate_id}` | Get cert details | Student only |
| POST | `/verify/{certificate_id}` | Verify/reject cert | Admin only |
| GET | `/admin/pending` | Get pending certs | Admin only |

## Example Usage

### 1. Register and Login

```bash
# Register
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123",
    "role": "student"
  }'

# Login
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "student"
  }
}
```

### 2. Submit Test Answers

```bash
curl -X POST "http://localhost:8000/api/tests/submit-answers" \
  -H "Authorization: Bearer <access_token>" \
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
      }
    ]
  }'
```

Response includes weak topics and recommendations.

### 3. Create Placement Profile

```bash
curl -X POST "http://localhost:8000/api/placement/profile" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "skills": ["React", "Node.js", "JavaScript", "Python", "Django"],
    "projects": ["E-commerce site", "Blog API"],
    "cgpa": 3.8,
    "experience": "2 years internship"
  }'
```

Response includes best-fit domain: `Web` with domain scores.

### 4. Submit GDPI Response

```bash
curl -X POST "http://localhost:8000/api/gdpi/submit" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "responses": [
      {
        "question_id": 1,
        "response_text": "I am a passionate software developer with skills in full-stack development. My career goal is to become a senior engineer working on scalable systems."
      }
    ]
  }'
```

### 5. Upload Certificate

```bash
curl -X POST "http://localhost:8000/api/certificates/upload" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "course_name": "AWS Solutions Architect",
    "organization": "Amazon Web Services",
    "issued_date": "2023-06-15",
    "expiry_date": "2026-06-15",
    "notes": "Professional certification"
  }'
```

## Sample Test Credentials

After running `seed_data.py`:

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

## Rule-Based Logic Details

### Weak Topic Analysis
- Compares student answers (case-insensitive) with correct answers
- Calculates percentage score per topic
- Marks topics with score < 70% as weak
- Generates recommendations based on score level

### GDPI Evaluation
- Tokenizes response text
- Counts keyword matches from a predefined list
- Scores: (matched_keywords / total_keywords) × 10
- Bonus points for detailed responses (50+ words)
- Generates feedback based on score range

### Placement Segregation
- Matches student skills against domain-specific keywords
- Domain score = (matched_skills / domain_keywords) × 100
- Best-fit domain has highest score
- Score below 20% defaults to "Generalist"
- Top students ranked by CGPA within domain

### Certificate Validation
- Validates course name and organization (non-empty)
- Validates date format (YYYY-MM-DD)
- Ensures expiry date >= issued date
- All validation errors reported together

## Error Handling

The API returns standard HTTP status codes:

- `200`: Success
- `201`: Created
- `400`: Bad Request (validation error)
- `401`: Unauthorized (invalid/missing token)
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found
- `500`: Internal Server Error

Error response format:
```json
{
  "detail": "Error message describing what went wrong"
}
```

## Environment Configuration

Create a `.env` file:

```env
# Database
DATABASE_URL=postgresql://aios_user:aios_password@localhost:5432/aios_db
SQL_ECHO=False

# JWT
JWT_SECRET=your-secret-key-change-in-production

# CORS
ALLOWED_ORIGINS=http://localhost,http://localhost:3000,http://localhost:8000
```

## Production Deployment

1. **Set secure JWT secret**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Use environment variables for sensitive data**
   - Never commit `.env` file
   - Use secrets management service

3. **Enable HTTPS**
   - Use reverse proxy (nginx/Apache)
   - Obtain SSL certificate

4. **Database**
   - Use managed PostgreSQL service
   - Enable backups
   - Use strong passwords

5. **Run with multiple workers**
   ```bash
   gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
   ```

## Development

### Running Tests
```bash
# Tests not included in MVP but structure ready
pytest
```

### Code Quality
```bash
# Format code
black app/

# Lint
flake8 app/

# Type checking
mypy app/
```

## Troubleshooting

### Database Connection Error
```
Error: could not translate host name "localhost" to address
```
Solution: Ensure PostgreSQL is running and DATABASE_URL is correct

### JWT Token Expired
```
Error: Token has expired
```
Solution: Login again to get a new token

### Permission Denied
```
Error: Admin access required
```
Solution: Ensure you have the correct role for the endpoint

## Future Enhancements

1. **AI Integration**
   - NLP-based answer evaluation
   - Personalized learning recommendations
   - Automated weak topic identification

2. **Real Interview System**
   - Video recording of GDPI responses
   - Facial expression analysis
   - Speech-to-text evaluation

3. **Advanced Analytics**
   - Learning analytics dashboard
   - Predictive placement success
   - Peer comparison metrics

4. **Additional Features**
   - Discussion forums
   - Resource recommendations
   - Progress tracking
   - Notification system

## License

This project is part of the AIOS (AI-driven College Ecosystem) initiative.

## Support

For issues and questions:
- Check the troubleshooting section
- Review API documentation at `/docs`
- Check database connection settings
- Ensure all dependencies are installed

---

**Version**: 1.0.0  
**Last Updated**: November 2025
