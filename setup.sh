#!/bin/bash

# RAG Application Setup Script
# This script automates the setup process for local development

echo "================================================"
echo "RAG Application Setup"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

echo "✅ Node.js found: $(node --version)"
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed successfully"
else
    echo "❌ Failed to install Python dependencies"
    exit 1
fi
echo ""

# Build frontend
echo "🎨 Building frontend..."
cd frontend
npm install
if [ $? -eq 0 ]; then
    echo "✅ Frontend dependencies installed"
else
    echo "❌ Failed to install frontend dependencies"
    exit 1
fi

npm run build
if [ $? -eq 0 ]; then
    echo "✅ Frontend built successfully"
else
    echo "❌ Failed to build frontend"
    exit 1
fi
cd ..
echo ""

# Check for data files
DATA_COUNT=$(find data -name "*.json" 2>/dev/null | wc -l)
if [ $DATA_COUNT -eq 0 ]; then
    echo "⚠️  Warning: No JSON files found in data/ folder"
    echo "   Please add your data files to data/ folder before running the app"
else
    echo "✅ Found $DATA_COUNT JSON file(s) in data/ folder"
fi
echo ""

echo "================================================"
echo "Setup Complete! 🎉"
echo "================================================"
echo ""
echo "To start the application:"
echo "  python app.py"
echo ""
echo "Then visit: http://localhost:8000"
echo ""
echo "To deploy to Render:"
echo "  See DEPLOYMENT.md for detailed instructions"
echo ""
