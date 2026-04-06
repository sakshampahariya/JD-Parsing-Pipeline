#!/bin/bash

# Job Description Pipeline - Quick Start Script
# This script helps set up the Flask application quickly

echo "================================"
echo "Job Description Pipeline Setup"
echo "================================"
echo ""

# Check Python installation
if ! command -v python &> /dev/null
then
    if ! command -v python3 &> /dev/null
    then
        echo "❌ Python is not installed. Please install Python 3.8 or higher."
        exit 1
    fi
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

echo "✓ Python found: $($PYTHON_CMD --version)"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
$PYTHON_CMD -m venv venv

# Activate virtual environment
echo "✓ Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo "📥 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env from .env.example if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your API keys:"
    echo "   - OPENAI_API_KEY"
    echo "   - SUPABASE_URL"
    echo "   - SUPABASE_KEY"
fi

# Create uploads directory
echo "📁 Creating uploads directory..."
mkdir -p uploads

echo ""
echo "================================"
echo "✓ Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your credentials"
echo "2. Run: python app.py"
echo "3. Open: http://localhost:5000"
echo ""
