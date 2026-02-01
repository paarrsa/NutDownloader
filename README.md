# Telegram Video Downloader Bot 🎬

A powerful Telegram bot that downloads videos from 1000+ websites using yt-dlp. Supports Persian language with easy multi-language expansion.

## Features ✨

- 📥 Download videos from YouTube, Instagram, Twitter, TikTok, and 1000+ websites
- 🇮🇷 Persian language interface
- 🌍 Multi-language support (easily add more languages)
- 🎵 Audio-only download option
- 📊 Multiple quality/format options
- ⚡ Fast and efficient
- 🔄 Auto-updates using latest yt-dlp

## Project Structure

```
telegram-ytdlp-bot/
├── bot.py                      # Main bot file
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── config/
│   ├── __init__.py
│   └── settings.py            # Configuration settings
├── handlers/
│   ├── __init__.py
│   └── message_handlers.py   # Telegram message handlers
├── utils/
│   ├── __init__.py
│   ├── localization.py       # Multi-language support
│   └── downloader.py         # yt-dlp wrapper
├── locales/
│   ├── fa.json              # Persian translations
│   └── en.json              # English translations
└── downloads/               # Temporary download directory
```

## Installation on VPS 🚀

### Prerequisites

- Ubuntu 20.04+ (or Debian-based system)
- Python 3.8 or higher
- FFmpeg (for audio conversion)
- A Telegram Bot Token from [@BotFather](https://t.me/BotFather)

### Step 1: Connect to Your VPS

```bash
ssh your_username@your_vps_ip
```

### Step 2: Update System Packages

```bash
sudo apt update
sudo apt upgrade -y
```

### Step 3: Install Required System Packages

```bash
# Install Python, pip, and FFmpeg
sudo apt install -y python3 python3-pip python3-venv ffmpeg git

# Verify installations
python3 --version
ffmpeg -version
```

### Step 4: Clone or Upload the Bot

**Option A: Using Git (if you have a repository)**
```bash
cd ~
git clone https://github.com/yourusername/telegram-ytdlp-bot.git
cd telegram-ytdlp-bot
```

**Option B: Manual Upload**
```bash
# Create directory
mkdir -p ~/telegram-ytdlp-bot
cd ~/telegram-ytdlp-bot

# Upload files using SCP from your local machine:
# scp -r /path/to/telegram-ytdlp-bot/* your_username@your_vps_ip:~/telegram-ytdlp-bot/
```

### Step 5: Create Virtual Environment

```bash
cd ~/telegram-ytdlp-bot
python3 -m venv venv
source venv/bin/activate
```

### Step 6: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 7: Configure the Bot

Create a `.env` file or edit `config/settings.py`:

```bash
# Copy example environment file
cp .env.example .env

# Edit with your bot token
nano .env
```

Add your bot token:
```
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

Or edit `config/settings.py` directly:
```bash
nano config/settings.py
```

Change this line:
```python
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
```

### Step 8: Test the Bot

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run the bot
python bot.py
```

You should see: `Starting bot...`

Test it by sending `/start` to your bot on Telegram. If it works, press `Ctrl+C` to stop it.

### Step 9: Set Up Auto-Start with Systemd

Create a systemd service to run the bot automatically:

```bash
# Edit the service file with correct paths
nano telegram-bot.service
```

Update these lines:
```ini
User=YOUR_USERNAME  # Replace with your username (run: whoami)
WorkingDirectory=/home/YOUR_USERNAME/telegram-ytdlp-bot
Environment="PATH=/home/YOUR_USERNAME/telegram-ytdlp-bot/venv/bin"
ExecStart=/home/YOUR_USERNAME/telegram-ytdlp-bot/venv/bin/python bot.py
```

Copy the service file:
```bash
sudo cp telegram-bot.service /etc/systemd/system/telegram-bot.service
```

Enable and start the service:
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service to start on boot
sudo systemctl enable telegram-bot.service

# Start the service
sudo systemctl start telegram-bot.service

# Check status
sudo systemctl status telegram-bot.service
```

### Step 10: Useful Commands

```bash
# Check bot status
sudo systemctl status telegram-bot.service

# Stop the bot
sudo systemctl stop telegram-bot.service

# Restart the bot
sudo systemctl restart telegram-bot.service

# View logs (live)
sudo journalctl -u telegram-bot.service -f

# View last 100 lines of logs
sudo journalctl -u telegram-bot.service -n 100
```

## Updating the Bot 🔄

To update yt-dlp and the bot:

```bash
cd ~/telegram-ytdlp-bot
source venv/bin/activate

# Update yt-dlp
pip install --upgrade yt-dlp

# If you updated code, restart the service
sudo systemctl restart telegram-bot.service
```

## Adding New Languages 🌍

1. Create a new JSON file in `locales/` directory:
```bash
nano locales/ar.json  # For Arabic
```

2. Copy the structure from `fa.json` and translate all strings

3. Update `config/settings.py` to change default language:
```python
DEFAULT_LANGUAGE = 'ar'  # or 'en', 'fa', etc.
```

4. Restart the bot:
```bash
sudo systemctl restart telegram-bot.service
```

## Troubleshooting 🔧

### Bot doesn't respond
1. Check if service is running: `sudo systemctl status telegram-bot.service`
2. Check logs: `sudo journalctl -u telegram-bot.service -n 50`
3. Verify bot token is correct
4. Ensure firewall allows outbound connections

### Download fails
1. Verify FFmpeg is installed: `ffmpeg -version`
2. Check disk space: `df -h`
3. Update yt-dlp: `pip install --upgrade yt-dlp`

### Service won't start
1. Check file permissions: `ls -la ~/telegram-ytdlp-bot`
2. Verify paths in service file are correct
3. Check logs: `sudo journalctl -u telegram-bot.service -n 50`

## Configuration Options ⚙️

Edit `config/settings.py`:

```python
# Change default language
DEFAULT_LANGUAGE = 'fa'  # 'en', 'fa', or any language code you add

# Change max file size (in bytes)
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Change download directory
DOWNLOAD_DIR = BASE_DIR / 'downloads'
```

## Security Recommendations 🔒

1. **Keep your bot token secure** - Never share it publicly
2. **Regular updates** - Keep yt-dlp and dependencies updated
3. **Monitor disk usage** - Downloads folder can grow large
4. **Set up log rotation** - Prevent logs from filling disk

### Clean up downloads folder regularly:

Create a cron job:
```bash
crontab -e
```

Add this line to clean downloads older than 1 hour:
```
0 * * * * find /home/YOUR_USERNAME/telegram-ytdlp-bot/downloads -type f -mmin +60 -delete
```

## Getting Your Bot Token 🤖

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Follow the instructions:
   - Choose a name for your bot
   - Choose a username (must end with 'bot')
4. Copy the API token provided
5. Paste it in `.env` file or `config/settings.py`

## Supported Websites 🌐

The bot supports 1000+ websites including:
- YouTube
- Instagram
- Twitter/X
- TikTok
- Facebook
- Vimeo
- Dailymotion
- Reddit
- And many more!

For a full list, check: https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md

## License 📄

This project uses yt-dlp which is licensed under the Unlicense.

## Support 💬

If you encounter issues:
1. Check the logs: `sudo journalctl -u telegram-bot.service -f`
2. Update yt-dlp: `pip install --upgrade yt-dlp`
3. Restart the bot: `sudo systemctl restart telegram-bot.service`

---

Made with ❤️ for easy video downloading