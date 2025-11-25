# CampusAI — Technical Requirements Document (TRD)

**Version:** 1.0  
**Date:** November 2025  
**Document Owner:** Engineering Team  
**Status:** Draft for Review

---

## 1. Technical Overview

### 1.1 Purpose

This Technical Requirements Document defines the complete technical specifications, architecture, and implementation guidelines for CampusAI—an AI-powered smart campus ecosystem.

### 1.2 Core Technology Stack

| Layer | Technologies |
|-------|-------------|
| Frontend | React 18+, TypeScript, TailwindCSS, WebRTC |
| Backend | FastAPI (Python 3.11+), Pydantic, SQLAlchemy |
| AI/ML | Llama 3.1, Mistral, Whisper, Sentence Transformers |
| Database | PostgreSQL 15+, MongoDB 7+, Redis 7+ |
| Search | Elasticsearch 8+ / Meilisearch |
| Storage | MinIO / AWS S3 |
| Infrastructure | Docker, Kubernetes, Nginx |

---

## 2. High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      PRESENTATION TIER                          │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐ │
│  │  Student   │  │  Faculty   │  │   Admin    │  │   Voice    │ │
│  │  Portal    │  │  Portal    │  │   Panel    │  │ Interface  │ │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘ │
└────────┼───────────────┼───────────────┼───────────────┼────────┘
         └───────────────┴───────┬───────┴───────────────┘
                                 ▼
┌──────────────────────────────────────────────────────────────────┐
│                    API GATEWAY (Nginx/Kong)                      │
│    SSL Termination • Rate Limiting • JWT Validation • Routing    │
└────────────────────────────────┬─────────────────────────────────┘
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                     APPLICATION TIER                            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │   Auth   │ │ Schedule │ │   Test   │ │Placement │            │
│  │ Service  │ │ Service  │ │ Service  │ │ Service  │            │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │  Cert    │ │  Notif   │ │  Career  │ │  Voice   │            │
│  │ Service  │ │ Service  │ │ Training │ │Assistant │            │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘            │
└────────────────────────────────┬────────────────────────────────┘
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                        AI/ML TIER                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │ ASR Engine  │  │ LLM Service │  │RAG Pipeline │              │
│  │  (Whisper)  │  │(Llama/Mistr)│  │ (Qdrant)    │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  Scoring    │  │ OCR Service │  │Model Manager│              │
│  │  Engine     │  │  (DocTR)    │  │   (vLLM)    │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
└────────────────────────────────┬────────────────────────────────┘
                                 ▼
┌─────────────────────────────────────────────────────────────────┐
│                        DATA TIER                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │PostgreSQL│ │ MongoDB  │ │  Redis   │ │Vector DB │            │
│  │(Relation)│ │(Document)│ │ (Cache)  │ │ (Qdrant) │            │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘            │
│  ┌────────────────────────┐  ┌────────────────────────┐         │
│  │   Object Storage       │  │   Search Engine        │         │
│  │   (MinIO/S3)           │  │   (Elasticsearch)      │         │
│  └────────────────────────┘  └────────────────────────┘         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. AI/ML Model Requirements

### 3.1 Automatic Speech Recognition (ASR)

**Model**: OpenAI Whisper Large-v3 (Self-hosted)

| Specification | Requirement |
|---------------|-------------|
| Accuracy Target | WER < 10% |
| Latency | < 5s per minute of audio |
| Throughput | 50 concurrent transcriptions |

**Features**: Real-time streaming, speaker diarization, punctuation restoration

### 3.2 Large Language Models (LLMs)

**Primary**: Llama 3.1 8B Instruct | **Fallback**: Mistral 7B Instruct

| Use Case | Model | Max Tokens | Temp |
|----------|-------|------------|------|
| Summarization | Llama 3.1 8B | 4096 | 0.3 |
| Voice Q&A | Llama 3.1 8B | 1024 | 0.5 |
| Interview | Llama 3.1 8B | 2048 | 0.7 |
| GDPI Moderation | Mistral 7B | 2048 | 0.6 |

**Deployment**: vLLM with AWQ 4-bit quantization, 85% GPU memory utilization

### 3.3 Embedding Models

**Model**: Sentence Transformers (all-MiniLM-L6-v2)

| Spec | Value |
|------|-------|
| Dimensions | 384 |
| Max Sequence | 512 tokens |
| Latency | < 50ms/document |

### 3.4 RAG Pipeline

```
Query → Embedding → Vector Search (Top-5) → Re-Ranking → LLM Generation → Response
```

**Config**: Qdrant vector store, chunk size 512, overlap 50, similarity threshold 0.7

### 3.5 Evaluation Models

**GDPI Scoring Dimensions**: Content (25%), Communication (25%), Logic (20%), Interaction (15%), Leadership (15%)

**Interview Scoring Dimensions**: Technical Accuracy (30%), Communication (25%), Problem Solving (20%), Confidence (15%), Domain Knowledge (10%)

---

## 4. Backend Specifications

### 4.1 API Endpoints Summary

#### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/register` | User registration |
| POST | `/api/v1/auth/login` | Login, returns JWT |
| POST | `/api/v1/auth/refresh` | Refresh token |
| GET | `/api/v1/auth/me` | Current user info |

#### Schedule Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/schedules/today` | Today's schedule |
| GET | `/api/v1/schedules/next` | Next class |
| POST | `/api/v1/schedules` | Create (Admin) |
| PUT | `/api/v1/schedules/{id}` | Update (Admin) |
| GET | `/api/v1/schedules/conflicts` | Check conflicts |

#### Voice & Transcription
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/voice/query` | Process voice query |
| WS | `/api/v1/voice/stream` | Real-time voice |
| POST | `/api/v1/transcripts/upload` | Upload audio |
| GET | `/api/v1/transcripts/{id}/summary` | Get summary |

#### Assessment & Placement
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/assessments` | Create test |
| POST | `/api/v1/assessments/{id}/submit` | Submit answers |
| GET | `/api/v1/assessments/weak-topics` | Weak topic report |
| GET | `/api/v1/placements/skill-groups` | Student groupings |
| POST | `/api/v1/certificates/upload` | Upload certificate |

#### Career Training
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/gdpi/sessions` | Start GDPI |
| POST | `/api/v1/gdpi/sessions/{id}/respond` | Submit response |
| POST | `/api/v1/interviews/start` | Start interview |
| GET | `/api/v1/interviews/{id}/report` | Get report |

### 4.2 Authentication (JWT)

```python
ACCESS_TOKEN_EXPIRE = 30 minutes
REFRESH_TOKEN_EXPIRE = 7 days
ALGORITHM = "HS256"

# Token Payload
{
  "sub": "user_id",
  "email": "user@campus.edu",
  "role": "student",
  "exp": 1699999999
}
```

### 4.3 RBAC Permission Matrix

| Resource | Student | Faculty | Admin |
|----------|---------|---------|-------|
| Schedule Read | Own | Own+Class | All |
| Schedule Write | ✗ | ✗ | ✓ |
| Assessment Take | ✓ | ✗ | ✗ |
| Assessment Create | ✗ | ✓ | ✓ |
| Transcript Read | Own | Own+Class | All |
| User Management | ✗ | ✗ | ✓ |

---

## 5. Database Schema

### 5.1 PostgreSQL (Relational)

```sql
-- Core Tables
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'student',
    first_name VARCHAR(100), last_name VARCHAR(100),
    department_id UUID REFERENCES departments(id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE student_profiles (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    enrollment_number VARCHAR(50) UNIQUE,
    batch_year INT, semester INT, cgpa DECIMAL(3,2),
    skill_domain VARCHAR(100),
    placement_status VARCHAR(50) DEFAULT 'not_placed'
);

CREATE TABLE faculty_profiles (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    employee_id VARCHAR(50) UNIQUE,
    designation VARCHAR(100), specialization VARCHAR(255)
);

CREATE TABLE courses (
    id UUID PRIMARY KEY,
    code VARCHAR(20) UNIQUE, name VARCHAR(255),
    department_id UUID REFERENCES departments(id),
    credits INT, semester INT
);

CREATE TABLE schedules (
    id UUID PRIMARY KEY,
    course_id UUID REFERENCES courses(id),
    faculty_id UUID REFERENCES users(id),
    room VARCHAR(50), day_of_week INT,
    start_time TIME, end_time TIME,
    semester INT, batch_year INT, is_active BOOLEAN
);

CREATE TABLE assessments (
    id UUID PRIMARY KEY,
    course_id UUID REFERENCES courses(id),
    faculty_id UUID REFERENCES users(id),
    title VARCHAR(255), type VARCHAR(50),
    questions JSONB, created_at TIMESTAMP
);

CREATE TABLE assessment_results (
    id UUID PRIMARY KEY,
    assessment_id UUID REFERENCES assessments(id),
    student_id UUID REFERENCES users(id),
    answers JSONB, score DECIMAL(5,2),
    weak_topics JSONB, submitted_at TIMESTAMP
);

CREATE TABLE certificates (
    id UUID PRIMARY KEY,
    student_id UUID REFERENCES users(id),
    title VARCHAR(255), issuer VARCHAR(255),
    category VARCHAR(100), issue_date DATE,
    file_path VARCHAR(500), extracted_data JSONB,
    validation_status VARCHAR(50), created_at TIMESTAMP
);

-- Indexes
CREATE INDEX idx_schedules_day ON schedules(day_of_week);
CREATE INDEX idx_schedules_faculty ON schedules(faculty_id);
CREATE INDEX idx_results_student ON assessment_results(student_id);
CREATE INDEX idx_certificates_student ON certificates(student_id);
```

### 5.2 MongoDB (Documents)

```javascript
// transcripts collection
{
  _id: ObjectId,
  lecture_id: UUID,
  course_id: UUID,
  faculty_id: UUID,
  audio_file_path: String,
  transcript: { full_text: String, segments: [{start, end, text, speaker}] },
  summary: { key_points: [String], full_summary: String },
  embeddings_stored: Boolean,
  created_at: Date
}

// interview_sessions collection
{
  _id: ObjectId,
  student_id: UUID,
  type: "technical" | "hr" | "managerial",
  domain: String,
  conversation: [{ role: String, content: String, timestamp: Date }],
  scores: { technical: Number, communication: Number, confidence: Number },
  feedback: String, personality_traits: [String],
  created_at: Date, completed_at: Date
}

// gdpi_sessions collection
{
  _id: ObjectId,
  topic: String, participants: [UUID],
  discussion: [{ participant_id, content, timestamp, scores }],
  individual_scores: [{ participant_id, content: Number, communication: Number }],
  leaderboard_position: Number,
  created_at: Date
}
```

---

## 6. Admin Panel Technical Requirements

### 6.1 Features

| Module | Capabilities |
|--------|-------------|
| Dashboard | KPIs, charts, system health, recent activity |
| User Management | CRUD users, role assignment, bulk import |
| Schedule Builder | Drag-drop interface, conflict detection, bulk operations |
| Analytics | Class performance, weak topics, placement stats |
| Certificate Review | Pending validations, manual override |
| System Config | Feature flags, API keys, notifications |

### 6.2 Tech Stack
- **Framework**: React 18 + TypeScript
- **UI Library**: shadcn/ui + TailwindCSS
- **State**: React Query + Zustand
- **Charts**: Recharts
- **Tables**: TanStack Table

---

## 7. Data Flow Diagrams

### 7.1 Voice Query Flow
```
User Speech → Browser Mic → WebSocket → ASR (Whisper) → Text
    → NLU (Intent Classification) → Query Handler → Database
    → Response Generator (LLM) → TTS → Audio Response
```

### 7.2 Transcription Flow
```
Audio Upload → S3 Storage → Queue (Redis) → ASR Worker
    → Raw Transcript → Summarizer (LLM) → Embeddings
    → Vector Store + MongoDB → Notification
```

### 7.3 Interview Flow
```
Start Session → Domain Selection → LLM Generates Question
    → User Response (Voice/Text) → ASR → Answer Analysis
    → Scoring Engine → Next Question (Adaptive) → [Loop]
    → Final Report Generation → Store Results
```

---

## 8. DevOps Requirements

### 8.1 Docker Configuration

```yaml
# docker-compose.yml (simplified)
services:
  api:
    build: ./backend
    ports: ["8000:8000"]
    depends_on: [postgres, redis, mongodb]
    
  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    
  ml-service:
    build: ./ml
    runtime: nvidia
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]
    
  postgres:
    image: postgres:15
    volumes: [postgres_data:/var/lib/postgresql/data]
    
  mongodb:
    image: mongo:7
    volumes: [mongo_data:/data/db]
    
  redis:
    image: redis:7-alpine
    
  qdrant:
    image: qdrant/qdrant
    volumes: [qdrant_data:/qdrant/storage]
```

### 8.2 CI/CD Pipeline

```yaml
# .github/workflows/main.yml
stages:
  - lint-test:
      - ruff, mypy (Python)
      - eslint, tsc (TypeScript)
      - pytest (80% coverage)
      - jest (React components)
      
  - build:
      - Docker images
      - Push to registry
      
  - deploy-staging:
      - Kubernetes apply
      - Run migrations
      - Health checks
      
  - deploy-production:
      - Manual approval
      - Blue-green deployment
      - Rollback on failure
```

### 8.3 Monitoring Stack

| Tool | Purpose |
|------|---------|
| Prometheus | Metrics collection |
| Grafana | Dashboards & alerts |
| Loki | Log aggregation |
| Jaeger | Distributed tracing |
| Sentry | Error tracking |

---

## 9. Security Requirements

### 9.1 Data Security

| Requirement | Implementation |
|-------------|----------------|
| Encryption in transit | TLS 1.3 mandatory |
| Encryption at rest | AES-256 for S3, PostgreSQL |
| Password storage | bcrypt (cost factor 12) |
| API authentication | JWT with RS256 |
| Rate limiting | 100 req/min per user |

### 9.2 Compliance

- OWASP Top 10 mitigation
- Input validation on all endpoints
- SQL injection prevention (parameterized queries)
- XSS prevention (content sanitization)
- CORS configured for allowed origins only
- Audit logging for sensitive operations

---

## 10. Performance Requirements

| Metric | Target |
|--------|--------|
| API Response (p95) | < 500ms |
| Page Load | < 2s |
| Voice Query E2E | < 3s |
| Transcription | < 5s per minute |
| Concurrent Users | 1,000 |
| Database Queries | < 100ms |

---

## 11. Scalability Strategy

### Horizontal Scaling
- Stateless API services behind load balancer
- Redis for session storage (not local memory)
- Database read replicas for queries
- CDN for static assets

### Vertical Scaling
- GPU instances for ML inference
- Connection pooling for databases
- Async processing for heavy operations

### Auto-scaling Rules
```yaml
metrics:
  - cpu_utilization > 70% for 5min → scale up
  - cpu_utilization < 30% for 10min → scale down
  - request_queue > 100 → scale up
  - gpu_memory > 85% → add ML instance
```

---

## 12. Testing Strategy

| Test Type | Coverage Target | Tools |
|-----------|----------------|-------|
| Unit Tests | 80% | pytest, jest |
| Integration | All API endpoints | pytest + httpx |
| E2E | Critical flows | Playwright |
| Load Testing | 2x expected load | Locust |
| Security | OWASP scan | ZAP, Trivy |
| ML Model | Accuracy benchmarks | Custom suite |

---

## 13. Future Enhancements

### Phase 2 (Months 7-9)
- Native mobile apps (React Native)
- Multi-language support (Hindi, Tamil, Telugu)
- SSO integration (SAML, LDAP)
- Real-time collaboration features

### Phase 3 (Months 10-12)
- ERP/LMS integrations
- Advanced analytics dashboard
- AI proctoring for exams
- Alumni network module

### Phase 4 (Year 2)
- Multi-tenant architecture
- Custom model fine-tuning per institution
- Predictive analytics (dropout risk, placement prediction)
- Mobile-first offline mode

---

*End of Technical Requirements Document*