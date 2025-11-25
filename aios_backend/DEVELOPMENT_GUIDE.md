# AIOS Backend - Development Guide

## Project Overview

AIOS Backend is a FastAPI application for a college AI ecosystem management system. It's a rule-based MVP (no AI/ML models) that handles:

- User authentication with JWT
- Test management and analysis
- GDPI mock interviews
- Placement profile segregation
- Certificate validation

## Architecture

### Layered Architecture

```
┌─────────────────────────────────────────┐
│         FastAPI Routes Layer            │
│    (Routes: auth, tests, gdpi, etc)    │
├─────────────────────────────────────────┤
│         Service Layer                   │
│  (Business logic, rule-based analysis) │
├─────────────────────────────────────────┤
│       Database Layer (SQLAlchemy)       │
│         (Models, ORM operations)        │
├─────────────────────────────────────────┤
│       PostgreSQL Database               │
└─────────────────────────────────────────┘
```

### Key Components

1. **Models** (`app/models/`)
   - Database schema definitions using SQLAlchemy
   - Relationships between tables

2. **Schemas** (`app/schemas/`)
   - Pydantic models for request/response validation
   - Type hints and documentation

3. **Services** (`app/services/`)
   - Business logic implementation
   - Rule-based calculations
   - Database operations

4. **Routes** (`app/routes/`)
   - API endpoint handlers
   - Request/response processing
   - Error handling

5. **Core** (`app/core/`)
   - Configuration
   - Database connection
   - Security utilities
   - Dependency injection

## Setting Up Development Environment

### macOS/Linux

```bash
# Clone repository
cd aios_backend

# Run setup script
chmod +x setup.sh
./setup.sh

# Update .env with your database credentials
nano .env

# Create PostgreSQL database
createuser -P aios_user
createdb -O aios_user aios_db

# Seed sample data
python seed_data.py

# Run development server
uvicorn app.main:app --reload
```

### Windows

```bash
# Clone repository
cd aios_backend

# Run setup script
setup.bat

# Update .env with your database credentials
# Then create PostgreSQL database using pgAdmin or psql

# Seed sample data
python seed_data.py

# Run development server
uvicorn app.main:app --reload
```

## Key Concepts

### Rule-Based Logic Examples

#### 1. Weak Topic Analysis
**File**: `app/services/weak_topic_service.py`

```python
# Simple case-insensitive comparison
is_correct = (student_answer.lower().strip() == correct_answer.lower().strip())

# Calculate score per topic
score_percentage = (correct_answers / total_questions) * 100

# Identify weak topics (threshold: 70%)
is_weak = score_percentage < 70
```

#### 2. GDPI Response Evaluation
**File**: `app/services/gdpi_service.py`

```python
# Count keyword matches
matched_keywords = [kw for kw in keywords if kw.lower() in response.lower()]

# Score calculation (0-10 scale)
score = (len(matched_keywords) / len(keywords)) * 10

# Bonus for detailed responses
if word_count >= 50:
    score = min(score + 1, 10)
```

#### 3. Placement Domain Matching
**File**: `app/services/placement_service.py`

```python
# Match skills to domain keywords
for domain, keywords in DOMAIN_KEYWORDS.items():
    matches = count_skill_keyword_matches(skills, keywords)
    domain_score = (matches / len(keywords)) * 100

# Best-fit domain has highest score
best_fit = max(domain_scores, key=domain_scores.get)
```

## Common Development Tasks

### Adding a New Endpoint

1. **Create service function** in `app/services/`:
```python
def new_service_function(db: Session, param: str):
    # Business logic here
    return result
```

2. **Create Pydantic schemas** in `app/schemas/__init__.py`:
```python
class NewRequestSchema(BaseModel):
    param: str

class NewResponseSchema(BaseModel):
    result: str
```

3. **Create route** in `app/routes/`:
```python
@router.post("/endpoint", response_model=NewResponseSchema)
async def new_endpoint(
    request: NewRequestSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = new_service_function(db, request.param)
    return result
```

### Adding a New Model

1. **Create model file** in `app/models/`:
```python
from sqlalchemy import Column, String, DateTime
from .base import Base

class NewTable(Base):
    __tablename__ = "new_tables"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

2. **Add to `app/models/__init__.py`**:
```python
from .new_table import NewTable
```

3. **Update database**:
```bash
# The init_db() function will create new tables automatically
```

### Adding Authentication to Endpoint

```python
from app.core.deps import get_current_user, require_role

# Public endpoint (no auth needed)
@router.get("/public")
async def public_endpoint():
    pass

# Authenticated endpoint
@router.get("/protected")
async def protected_endpoint(
    current_user: User = Depends(get_current_user),
):
    pass

# Role-based endpoint
@router.get("/admin-only")
async def admin_endpoint(
    current_user: User = Depends(require_role(UserRole.ADMIN)),
):
    pass
```

## Database Debugging

### Connect to Database

```bash
psql -U aios_user -d aios_db
```

### Useful SQL Queries

```sql
-- List all users
SELECT id, name, email, role FROM users;

-- List all tests
SELECT id, title, created_by FROM tests;

-- See weak topic reports
SELECT * FROM weak_topic_reports WHERE is_weak = 1;

-- List GDPI responses with scores
SELECT sr.id, sr.student_id, sr.score, sr.feedback 
FROM gdpi_responses sr 
ORDER BY sr.score DESC;

-- Get placement profiles by domain
SELECT sp.id, sp.student_id, sp.best_fit_domain, sp.cgpa 
FROM placement_profiles sp 
WHERE sp.best_fit_domain = 'Web' 
ORDER BY sp.cgpa DESC;

-- Verify certificates status
SELECT id, course_name, verification_status FROM certificates;
```

### View Database in SQL Logs

Set `SQL_ECHO=True` in `.env` to see all SQL queries in console.

## Error Handling

### Common Errors and Solutions

#### 1. Database Connection Error
```
Error: could not translate host name "localhost" to address
```
**Solution**: Check PostgreSQL is running and DATABASE_URL is correct

#### 2. Table Already Exists
```
Error: (psycopg2.errors.DuplicateTable) relation "users" already exists
```
**Solution**: Drop and recreate database:
```bash
dropdb aios_db
createdb -O aios_user aios_db
python seed_data.py
```

#### 3. JWT Token Invalid
```
Error: Invalid token
```
**Solution**: 
- Ensure JWT_SECRET is the same as the one used to create token
- Check token hasn't expired (30 minutes)

#### 4. Permission Denied
```
Error: Admin access required
```
**Solution**: Ensure user has correct role for endpoint

## Testing

### Manual Testing with curl

```bash
# Login
TOKEN=$(curl -s -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"amit@student.aios.edu","password":"student123"}' \
  | jq -r '.access_token')

# Test protected endpoint
curl -X GET "http://localhost:8000/api/auth/me" \
  -H "Authorization: Bearer $TOKEN"
```

### Using Swagger UI

Visit `http://localhost:8000/docs` and use the interactive interface:
1. Click on endpoint
2. Click "Try it out"
3. Enter parameters
4. Click "Execute"

## Performance Tips

1. **Database Indexing**
   - Frequently searched fields are already indexed
   - Add more if needed in model definition

2. **Query Optimization**
   - Use `.filter()` before executing
   - Use `.first()` instead of `.all()` when possible

3. **Connection Pooling**
   - Configured in `app/core/database.py`
   - Adjust pool size for production

4. **Caching** (Future)
   - Consider Redis for frequently accessed data
   - Cache DOMAIN_KEYWORDS and other constants

## Production Deployment

### Environment Setup

```bash
# Generate secure JWT secret
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Update .env
DATABASE_URL=postgresql://prod_user:secure_password@prod_host:5432/prod_db
JWT_SECRET=<generated_secure_secret>
```

### Run with Production Settings

```bash
# Using gunicorn with 4 workers
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

### Using Docker (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t aios-backend .
docker run -p 8000:8000 --env-file .env aios-backend
```

## Code Quality

### Code Style

```bash
# Format code with black
pip install black
black app/

# Lint with flake8
pip install flake8
flake8 app/

# Type checking with mypy
pip install mypy
mypy app/
```

### Project Structure Best Practices

1. **Keep services thin** - Only business logic
2. **Keep routes simple** - Just request/response handling
3. **Use dependency injection** - For database, auth, config
4. **Document functions** - Docstrings for all public functions
5. **Handle errors gracefully** - Return meaningful error messages

## Useful Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [JWT Authentication](https://pyjwt.readthedocs.io/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## Troubleshooting Checklist

- [ ] Python version 3.9+?
- [ ] Virtual environment activated?
- [ ] Dependencies installed? (`pip install -r requirements.txt`)
- [ ] PostgreSQL running?
- [ ] `.env` file configured?
- [ ] Database created and seeded?
- [ ] Port 8000 not in use?
- [ ] JWT_SECRET set in `.env`?

## Contributing

When adding features:
1. Create branch: `git checkout -b feature/feature-name`
2. Make changes
3. Test changes thoroughly
4. Commit: `git commit -m "Add feature"`
5. Push: `git push origin feature/feature-name`
6. Create pull request

---

**Need Help?**
- Check API_TESTING_GUIDE.md for endpoint examples
- Review README.md for architecture overview
- Check service files for business logic
- Use Swagger UI at `/docs` for interactive testing

---

**Last Updated**: November 2025
