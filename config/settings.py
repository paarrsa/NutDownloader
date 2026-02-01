import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Telegram Bot Token - Get from @BotFather
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# Default language
DEFAULT_LANGUAGE = 'fa'  # Persian

# Download settings
DOWNLOAD_DIR = BASE_DIR / 'downloads'
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB (Telegram limit for bots)

# yt-dlp settings
YTDLP_OPTIONS = {
    'format': 'best[filesize<50M]/best',  # Prefer files under 50MB
    'outtmpl': str(DOWNLOAD_DIR / '%(id)s.%(ext)s'),
    'quiet': True,
    'no_warnings': True,
    'extract_flat': False,
    'nocheckcertificate': True,
}

# Create downloads directory if it doesn't exist
DOWNLOAD_DIR.mkdir(exist_ok=True)

# Allowed video extensions
ALLOWED_VIDEO_EXTENSIONS = ['.mp4', '.mkv', '.webm', '.avi', '.mov']
ALLOWED_AUDIO_EXTENSIONS = ['.mp3', '.m4a', '.opus', '.ogg', '.wav']