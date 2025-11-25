import os
from datetime import timedelta

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# CORS Configuration
ALLOWED_ORIGINS = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
]

# Weak Topic Threshold
WEAK_TOPIC_THRESHOLD = 70.0  # Percentage below which a topic is considered weak

# Domain Keywords for Placement Segregation
DOMAIN_KEYWORDS = {
    "Web": ["react", "vue", "angular", "nodejs", "fastapi", "django", "html", "css", "javascript", "typescript", "web development"],
    "ML": ["machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn", "nlp", "computer vision", "python", "data science"],
    "Cloud": ["aws", "gcp", "azure", "docker", "kubernetes", "cloud", "devops", "jenkins", "ci/cd"],
    "Cybersecurity": ["security", "cryptography", "penetration testing", "network security", "ethical hacking", "firewall", "ssl"],
}
