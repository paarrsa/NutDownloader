#!/bin/bash

echo "================================================"
echo "Telegram Video Downloader Bot - Setup Script"
echo "================================================"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    echo "❌ Please do not run this script as root"
    exit 1
fi

# Check Python version
echo "🔍 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $PYTHON_VERSION found"

# Check FFmpeg
echo "🔍 Checking FFmpeg..."
if ! command -v ffmpeg &> /dev/null; then
    echo "❌ FFmpeg is not installed."
    echo "Install it with: sudo apt install ffmpeg"
    exit 1
fi
echo "✅ FFmpeg found"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your BOT_TOKEN"
    echo "   You can get a token from @BotFather on Telegram"
fi

# Create downloads directory
mkdir -p downloads

echo ""
echo "================================================"
echo "✅ Installation completed successfully!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your bot token:"
echo "   nano .env"
echo ""
echo "2. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "3. Run the bot:"
echo "   python bot.py"
echo ""
echo "For VPS deployment with auto-start, see README.md"
echo "================================================"