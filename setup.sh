#!/bin/bash

# Setup script for Resume Backend Manual

echo "🚀 Setting up Resume Backend Manual..."

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if python -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo "✅ Python $PYTHON_VERSION detected"
else
    echo "❌ Python 3.8+ is required. Current version: $PYTHON_VERSION"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your API keys and configuration"
fi

# Create logs directory
if [ ! -d "logs" ]; then
    echo "📝 Creating logs directory..."
    mkdir logs
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run: source venv/bin/activate"
echo "3. Run: python -m app.main"
echo ""
echo "🌐 API will be available at: http://localhost:8000"
echo "📖 API documentation at: http://localhost:8000/docs"
