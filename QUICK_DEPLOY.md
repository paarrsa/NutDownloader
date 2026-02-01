# Quick VPS Deployment Guide

## 🚀 Fast Setup (5 minutes)

### 1. Connect to VPS
```bash
ssh user@your_vps_ip
```

### 2. Install System Requirements
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv ffmpeg git
```

### 3. Upload Bot Files
```bash
# On your local machine, upload the bot:
scp -r telegram-ytdlp-bot user@your_vps_ip:~/

# Or create and upload manually:
mkdir -p ~/telegram-ytdlp-bot
cd ~/telegram-ytdlp-bot
# Then upload all files via SCP or FTP
```

### 4. Run Installation Script
```bash
cd ~/telegram-ytdlp-bot
chmod +x install.sh
./install.sh
```

### 5. Configure Bot Token
```bash
nano .env
# Add: BOT_TOKEN=your_token_from_botfather
```

### 6. Test the Bot
```bash
source venv/bin/activate
python bot.py
# Test on Telegram, then press Ctrl+C
```

### 7. Setup Auto-Start
```bash
# Edit service file with your username and paths
nano telegram-bot.service

# Update these lines:
# User=YOUR_USERNAME (use 'whoami' to find it)
# WorkingDirectory=/home/YOUR_USERNAME/telegram-ytdlp-bot
# Environment="PATH=/home/YOUR_USERNAME/telegram-ytdlp-bot/venv/bin"
# ExecStart=/home/YOUR_USERNAME/telegram-ytdlp-bot/venv/bin/python bot.py

# Install service
sudo cp telegram-bot.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable telegram-bot.service
sudo systemctl start telegram-bot.service

# Check status
sudo systemctl status telegram-bot.service
```

## ✅ Done!

Your bot is now running 24/7 on your VPS.

## Common Commands

```bash
# View logs
sudo journalctl -u telegram-bot.service -f

# Restart bot
sudo systemctl restart telegram-bot.service

# Stop bot
sudo systemctl stop telegram-bot.service

# Update yt-dlp
cd ~/telegram-ytdlp-bot
source venv/bin/activate
pip install --upgrade yt-dlp
sudo systemctl restart telegram-bot.service
```

## Get Bot Token

1. Open Telegram
2. Search for `@BotFather`
3. Send `/newbot`
4. Follow instructions
5. Copy the token
6. Add to `.env` file

## Troubleshooting

**Bot not responding?**
```bash
sudo systemctl status telegram-bot.service
sudo journalctl -u telegram-bot.service -n 50
```

**Download failing?**
```bash
# Update yt-dlp
pip install --upgrade yt-dlp
sudo systemctl restart telegram-bot.service
```

**Out of space?**
```bash
# Check space
df -h

# Clean old downloads
find ~/telegram-ytdlp-bot/downloads -type f -mmin +60 -delete
```