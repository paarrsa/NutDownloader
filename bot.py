#!/usr/bin/env python3
"""
Telegram Video Downloader Bot
Uses yt-dlp to download videos from 1000+ websites
"""

import logging
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)
from config.settings import BOT_TOKEN
from handlers.message_handlers import (
    start_command,
    help_command,
    cancel_command,
    formats_command,
    handle_message,
    handle_format_selection
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """Start the bot"""
    # Validate bot token
    if BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        logger.error("Please set your BOT_TOKEN in config/settings.py or as environment variable")
        return
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Register command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cancel", cancel_command))
    application.add_handler(CommandHandler("formats", formats_command))
    
    # Register callback query handler for inline buttons
    application.add_handler(CallbackQueryHandler(handle_format_selection))
    
    # Register message handler for text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Start the bot
    logger.info("Starting bot...")
    application.run_polling()


if __name__ == '__main__':
    main()