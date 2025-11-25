from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db
from app.core.config import ALLOWED_ORIGINS
from app.routes import auth, tests, gdpi, placement, certificates

# Initialize database
init_db()

# Create FastAPI app
app = FastAPI(
    title="AIOS Backend - College AI Ecosystem",
    description="Rule-based backend for college AI ecosystem MVP",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(tests.router)
app.include_router(gdpi.router)
app.include_router(placement.router)
app.include_router(certificates.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to AIOS Backend",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "AIOS Backend is running",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
