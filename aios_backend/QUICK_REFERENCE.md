# AIOS Backend - Quick Reference

## 🚀 Getting Started (5 Minutes)

### 1. Install & Setup
```bash
cd aios_backend
chmod +x setup.sh
./setup.sh
```

### 2. Configure Database
```bash
# Update .env with your PostgreSQL credentials
nano .env

# Create database
psql -U postgres -c "CREATE USER aios_user WITH PASSWORD 'aios_password';"
psql -U postgres -c "CREATE DATABASE aios_db OWNER aios_user;"
```

### 3. Seed Data & Run
```bash
python seed_data.py
uvicorn app.main:app --reload
```

### 4. Access API
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 📚 File Guide

| File/Folder | Purpose |
|-------------|---------|
| `app/main.py` | FastAPI application |
| `app/models/` | Database models |
| `app/routes/` | API endpoints |
| `app/services/` | Business logic |
| `app/core/` | Config, security, DB |
| `seed_data.py` | Sample data |
| `README.md` | Full documentation |
| `API_TESTING_GUIDE.md` | API examples |

---

## 🔑 Sample Credentials

```
Student: amit@student.aios.edu / student123
Faculty: rajesh@aios.edu / faculty123
Admin:   admin@aios.edu / admin123
```

---

## 🔗 Key Endpoints

### Authentication
```bash
POST   /api/auth/register
POST   /api/auth/login
GET    /api/auth/me
```

### Tests & Analysis
```bash
POST   /api/tests/create
POST   /api/tests/submit-answers
GET    /api/tests/analysis/{test_id}
```

### GDPI
```bash
GET    /api/gdpi/questions
POST   /api/gdpi/submit
```

### Placement
```bash
POST   /api/placement/profile
GET    /api/placement/profile
GET    /api/placement/domain/{domain}
```

### Certificates
```bash
POST   /api/certificates/upload
GET    /api/certificates/my-certificates
```

---

## 🧪 Quick Test Example

```bash
# 1. Login
TOKEN=$(curl -s -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"amit@student.aios.edu","password":"student123"}' \
  | jq -r '.access_token')

# 2. Submit test answers
curl -X POST "http://localhost:8000/api/tests/submit-answers" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "test_id": 1,
    "answers": [
      {"question_id": 1, "student_answer": "O(log n)"},
      {"question_id": 2, "student_answer": "Stack"}
    ]
  }'
```

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| Database connection error | Check PostgreSQL running, verify DATABASE_URL |
| Port 8000 in use | Change port: `uvicorn app.main:app --port 8001` |
| Token expired | Login again to get new token |
| Permission denied | Check user role for endpoint |
| Import errors | Ensure in virtual environment: `source venv/bin/activate` |

---

## 📖 Documentation

1. **README.md** - Installation, features, deployment
2. **DEVELOPMENT_GUIDE.md** - Architecture, tasks, debugging
3. **API_TESTING_GUIDE.md** - All endpoints with examples
4. **PROJECT_SUMMARY.md** - Overview and checklist

---

## ⚙️ Environment Variables (.env)

```env
DATABASE_URL=postgresql://aios_user:aios_password@localhost:5432/aios_db
JWT_SECRET=your-secret-key
SQL_ECHO=False
```

---

## 📊 Database Tables

- `users` - User accounts
- `tests` - Test papers  
- `questions` - Test questions
- `answers` - Student answers
- `weak_topic_reports` - Analysis results
- `gdpi_questions` - Interview questions
- `gdpi_responses` - Interview responses
- `placement_profiles` - Placement data
- `certificates` - Certificates

---

## 🎯 Rule-Based Logic

### Weak Topics: Score < 70% marked as weak
### GDPI: Keyword matches counted (0-10 scale)
### Placement: Best-fit domain based on skill matches
### Certificates: Validation of all required fields

---

## 🚢 Production Deployment

```bash
# Install gunicorn
pip install gunicorn

# Run with 4 workers
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

---

## 📞 Common Tasks

### Create New Test (Faculty)
```bash
POST /api/tests/create
{
  "title": "Test Title",
  "questions": [{"question_text": "Q?", "topic": "Math", "correct_answer": "A"}]
}
```

### Analyze Test (Student)
```bash
POST /api/tests/submit-answers
{
  "test_id": 1,
  "answers": [{"question_id": 1, "student_answer": "A"}]
}
```

### Create Placement Profile (Student)
```bash
POST /api/placement/profile
{
  "skills": ["Python", "React"],
  "cgpa": 3.8
}
```

---

## ✅ Verification Checklist

- [ ] Python 3.9+ installed
- [ ] PostgreSQL running
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Database created
- [ ] .env configured
- [ ] Sample data seeded
- [ ] Server running on port 8000
- [ ] Swagger UI accessible at /docs
- [ ] Sample credentials working

---

**Version**: 1.0.0 | **Status**: ✅ Complete | **Last Updated**: Nov 2025
