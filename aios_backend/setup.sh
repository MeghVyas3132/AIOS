#!/bin/bash

# AIOS Backend Setup Script
# This script helps set up the FastAPI backend locally

set -e

echo "🚀 AIOS Backend Setup"
echo "====================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check if PostgreSQL is available
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL client not found. Make sure PostgreSQL server is running."
    echo "   You can still proceed if you have PostgreSQL running elsewhere."
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created (update with your database credentials)"
fi

echo ""
echo "✅ Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Update .env file with your PostgreSQL credentials"
echo "2. Create PostgreSQL database:"
echo "   psql -U postgres -c \"CREATE USER aios_user WITH PASSWORD 'aios_password';\""
echo "   psql -U postgres -c \"CREATE DATABASE aios_db OWNER aios_user;\""
echo ""
echo "3. Seed sample data:"
echo "   python seed_data.py"
echo ""
echo "4. Run the server:"
echo "   uvicorn app.main:app --reload"
echo ""
echo "📖 API Documentation will be available at: http://localhost:8000/docs"
