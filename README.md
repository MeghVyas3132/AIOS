# 🎓 CampusAI — AI-Powered Smart Campus Ecosystem

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://reactjs.org)

CampusAI is a comprehensive AI-powered platform that transforms the educational experience through intelligent voice assistants, automated lecture summarization, adaptive assessments, and career training simulations.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running Locally](#-running-locally)
- [Deployment](#-deployment)
- [API Reference](#-api-reference)
- [Sample Prompts](#-sample-gdpi--interview-prompts)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

CampusAI addresses critical challenges in modern educational institutions by providing:

- **Intelligent Assistance**: Voice-activated schedule queries and campus information
- **Enhanced Learning**: Automated lecture transcription and AI-generated summaries
- **Personalized Assessment**: Adaptive tests that identify weak topics and recommend resources
- **Streamlined Administration**: Automated scheduling with conflict detection
- **Career Readiness**: AI-powered mock interviews and group discussion simulations

---

## ✨ Features

### 🎤 AI Assistant Features

| Feature | Description |
|---------|-------------|
| **Voice Assistant** | Natural language queries for schedules, classes, and campus info |
| **Class Summarization** | Audio-to-text transcription with AI-generated lecture summaries |
| **Test Analyzer** | Adaptive assessments with weak topic detection and personalized recommendations |

### 🏫 Campus Management Features

| Feature | Description |
|---------|-------------|
| **Schedule Management** | Admin panel for class allocation with conflict detection |
| **Placement Segregation** | AI-driven student categorization by skill domains |
| **Certificate Checker** | Automated validation and categorization of credentials |

### 💼 Career Training Features

| Feature | Description |
|---------|-------------|
| **GDPI Training Bot** | Gamified group discussion simulations with AI feedback |
| **Interview Engine** | Mock interviews with skill scoring and personality analysis |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                             │
│   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐        │
│   │ Student │   │ Faculty │   │  Admin  │   │  Voice  │        │
│   │  Portal │   │  Portal │   │  Panel  │   │   UI    │        │
│   └────┬────┘   └────┬────┘   └────┬────┘   └────┬────┘        │
└────────┼─────────────┼─────────────┼─────────────┼──────────────┘
         └─────────────┴──────┬──────┴─────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API GATEWAY                                │
│        (Nginx • JWT Auth • Rate Limiting • Load Balancing)      │
└─────────────────────────────┬───────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    APPLICATION SERVICES                         │
│  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐        │
│  │  Auth  │ │Schedule│ │  Test  │ │  GDPI  │ │  Voice │        │
│  └────────┘ └────────┘ └────────┘ └────────┘ └────────┘        │
└─────────────────────────────┬───────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      AI/ML SERVICES                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐        │
│  │  Whisper │  │ Llama 3  │  │   RAG    │  │ Scoring  │        │
│  │   ASR    │  │   LLM    │  │ Pipeline │  │  Engine  │        │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘        │
└─────────────────────────────┬───────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       DATA LAYER                                │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │PostgreSQL│ │ MongoDB  │ │  Redis   │ │  Qdrant  │           │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘           │
│  ┌─────────────────────┐  ┌─────────────────────┐              │
│  │    MinIO / S3       │  │    Elasticsearch    │              │
│  └─────────────────────┘  └─────────────────────┘              │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **ORM**: SQLAlchemy 2.0 + Alembic
- **Validation**: Pydantic v2
- **Task Queue**: Celery + Redis
- **WebSocket**: FastAPI WebSockets

### Frontend
- **Framework**: React 18 + TypeScript
- **Styling**: TailwindCSS
- **State Management**: React Query + Zustand
- **UI Components**: shadcn/ui
- **Voice**: Web Speech API + WebRTC

### AI/ML
- **ASR**: OpenAI Whisper (Large-v3)
- **LLM**: Llama 3.1 8B, Mistral 7B
- **Inference**: vLLM
- **Embeddings**: Sentence Transformers
- **Vector Store**: Qdrant
- **OCR**: DocTR / Tesseract

### Databases
- **Relational**: PostgreSQL 15+
- **Document**: MongoDB 7+
- **Cache**: Redis 7+
- **Search**: Elasticsearch 8+

### Infrastructure
- **Containers**: Docker + Docker Compose
- **Orchestration**: Kubernetes
- **Reverse Proxy**: Nginx
- **Storage**: MinIO / AWS S3

---

## 📦 Installation

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- NVIDIA GPU (recommended for ML)
- CUDA 11.8+ (for GPU inference)

### Clone Repository

```bash
git clone https://github.com/your-org/campusai.git
cd campusai
```

### Backend Setup

```bash
# Create virtual environment
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

### Frontend Setup

```bash
cd frontend
npm install
# or
yarn install
```

### Database Setup

```bash
# Start databases with Docker
docker-compose up -d postgres mongodb redis qdrant

# Run migrations
cd backend
alembic upgrade head

# Seed initial data (optional)
python scripts/seed_data.py
```

### RAG & Embeddings Setup

```bash
# Download embedding model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Initialize Qdrant collections
python scripts/init_vector_store.py
```

### ML Models Setup

```bash
# Download Whisper model
python -c "import whisper; whisper.load_model('large-v3')"

# Download LLM (requires ~16GB disk space)
# Option 1: Using Hugging Face
huggingface-cli download meta-llama/Llama-3.1-8B-Instruct

# Option 2: Using vLLM (recommended)
# Models are downloaded automatically on first run
```

---

## ⚙️ Configuration

### Environment Variables

Create `.env` files in both `backend/` and `frontend/` directories:

#### Backend `.env`

```env
# Application
APP_NAME=CampusAI
APP_ENV=development
DEBUG=true
SECRET_KEY=your-secret-key-min-32-chars

# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=campusai
POSTGRES_USER=campusai
POSTGRES_PASSWORD=your-password

# MongoDB
MONGO_URI=mongodb://localhost:27017/campusai

# Redis
REDIS_URL=redis://localhost:6379/0

# Vector Store
QDRANT_HOST=localhost
QDRANT_PORT=6333

# Object Storage
S3_ENDPOINT=http://localhost:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET=campusai

# AI/ML
WHISPER_MODEL=large-v3
LLM_MODEL=meta-llama/Llama-3.1-8B-Instruct
VLLM_HOST=localhost
VLLM_PORT=8001
EMBEDDING_MODEL=all-MiniLM-L6-v2

# JWT
JWT_SECRET_KEY=your-jwt-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

#### Frontend `.env`

```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_WS_URL=ws://localhost:8000/api/v1/voice/stream
VITE_APP_NAME=CampusAI
```

---

## 🚀 Running Locally

### Option 1: Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Option 2: Manual Start

#### Terminal 1: Backend API

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Terminal 2: ML Service (vLLM)

```bash
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Llama-3.1-8B-Instruct \
    --port 8001 \
    --quantization awq
```

#### Terminal 3: Celery Worker

```bash
cd backend
celery -A app.worker worker --loglevel=info
```

#### Terminal 4: Frontend

```bash
cd frontend
npm run dev
```

### Access Points

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| API Docs | http://localhost:8000/docs |
| API ReDoc | http://localhost:8000/redoc |
| Qdrant UI | http://localhost:6333/dashboard |
| MinIO Console | http://localhost:9001 |

---

## 🌐 Deployment

### Production with Docker

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes Deployment

```bash
# Apply configurations
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmaps/
kubectl apply -f k8s/secrets/
kubectl apply -f k8s/deployments/
kubectl apply -f k8s/services/
kubectl apply -f k8s/ingress.yaml

# Verify deployment
kubectl get pods -n campusai
```

### Environment-Specific Configs

```
k8s/
├── namespace.yaml
├── configmaps/
│   ├── app-config.yaml
│   └── ml-config.yaml
├── secrets/
│   └── app-secrets.yaml
├── deployments/
│   ├── api.yaml
│   ├── frontend.yaml
│   ├── ml-service.yaml
│   └── worker.yaml
├── services/
│   └── *.yaml
└── ingress.yaml
```

---

## 📚 API Reference

### Authentication

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "email": "student@campus.edu",
  "password": "password123"
}

Response:
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
```

### Voice Query

```http
POST /api/v1/voice/query
Authorization: Bearer {token}
Content-Type: application/json

{
  "text": "What is my schedule today?"
}

Response:
{
  "response": "You have 3 classes today...",
  "data": { "classes": [...] }
}
```

### Upload Lecture Audio

```http
POST /api/v1/transcripts/upload
Authorization: Bearer {token}
Content-Type: multipart/form-data

file: lecture.mp3
course_id: uuid

Response:
{
  "transcript_id": "uuid",
  "status": "processing"
}
```

### Start Mock Interview

```http
POST /api/v1/interviews/start
Authorization: Bearer {token}
Content-Type: application/json

{
  "type": "technical",
  "domain": "software_engineering"
}

Response:
{
  "session_id": "uuid",
  "question": "Tell me about yourself and your technical background."
}
```

Full API documentation available at `/docs` (Swagger) or `/redoc`.

---

## 🎯 Sample GDPI & Interview Prompts

### GDPI Topics

```
1. "Should AI replace teachers in classrooms?"
2. "Work from home vs. Office work - The future of employment"
3. "Is social media a boon or bane for students?"
4. "Climate change: Individual responsibility vs. Corporate accountability"
5. "The impact of automation on job markets in developing countries"
```

### Interview Question Bank

#### Technical (Software Engineering)
```
- "Explain the difference between REST and GraphQL APIs."
- "How would you design a URL shortening service?"
- "What are the SOLID principles? Give examples."
- "Explain the CAP theorem and its implications."
```

#### HR/Behavioral
```
- "Tell me about a time you failed and what you learned."
- "How do you handle disagreements with team members?"
- "Where do you see yourself in 5 years?"
- "Why should we hire you?"
```

#### Managerial
```
- "How would you handle an underperforming team member?"
- "Describe your approach to project prioritization."
- "How do you balance stakeholder expectations with team capacity?"
```

---

## 📁 Folder Structure

```
campusai/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # API endpoints
│   │   ├── core/            # Security, config
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   └── db/              # Database utilities
│   ├── ml/
│   │   ├── asr/             # Speech recognition
│   │   ├── llm/             # Language models
│   │   ├── rag/             # RAG pipeline
│   │   └── scoring/         # Evaluation
│   ├── tests/
│   ├── alembic/             # Migrations
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Route pages
│   │   ├── hooks/           # Custom hooks
│   │   ├── services/        # API clients
│   │   ├── store/           # State management
│   │   └── utils/           # Utilities
│   ├── public/
│   ├── package.json
│   └── Dockerfile
│
├── k8s/                     # Kubernetes configs
├── docker-compose.yml
├── docker-compose.prod.yml
└── README.md
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint + Prettier for TypeScript
- Write tests for new features (80% coverage minimum)
- Update documentation for API changes
- Use conventional commits

### Code Review Process

1. All PRs require at least one approval
2. CI checks must pass
3. No merge conflicts
4. Documentation updated

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- OpenAI Whisper for speech recognition
- Meta AI for Llama models
- Mistral AI for Mistral models
- FastAPI community
- All open-source contributors

---

**Built with ❤️ for Education**