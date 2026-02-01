from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from utils.localization import i18n
from utils.downloader import VideoDownloader
import os


# Initialize downloader
downloader = VideoDownloader()


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    await update.message.reply_text(i18n.get('welcome'))


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    await update.message.reply_text(i18n.get('help'))


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /cancel command"""
    # Clear user data
    context.user_data.clear()
    await update.message.reply_text(i18n.get('operation_cancelled'))


async def formats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /formats command - show available formats for last URL"""
    url = context.user_data.get('last_url')
    
    if not url:
        await update.message.reply_text(i18n.get('no_url_saved'))
        return
    
    # Send processing message
    processing_msg = await update.message.reply_text(i18n.get('extracting_info'))
    
    # Get formats
    formats = downloader.get_formats(url)
    
    if not formats:
        await processing_msg.edit_text(i18n.get('error_occurred', error='Could not extract formats'))
        return
    
    # Format list for display
    formats_text = ""
    for i, fmt in enumerate(formats[:20], 1):  # Limit to first 20 formats
        size = fmt['filesize']
        size_mb = f"{size / (1024 * 1024):.1f}MB" if size else "Unknown"
        
        formats_text += f"{i}. {fmt['format_id']} - {fmt['ext']} - {fmt['resolution']} ({size_mb})\n"
    
    await processing_msg.edit_text(i18n.get('formats_available', formats=formats_text))


async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming URLs"""
    url = update.message.text.strip()
    
    # Basic URL validation
    if not (url.startswith('http://') or url.startswith('https://')):
        await update.message.reply_text(i18n.get('invalid_url'))
        return
    
    # Save URL to user context
    context.user_data['last_url'] = url
    
    # Send processing message
    processing_msg = await update.message.reply_text(i18n.get('extracting_info'))
    
    # Extract video info
    info = downloader.extract_info(url)
    
    if not info:
        await processing_msg.edit_text(i18n.get('unsupported_site'))
        return
    
    # Get video title
    title = info.get('title', 'Unknown')
    context.user_data['video_title'] = title
    
    # Create format selection buttons
    keyboard = [
        [InlineKeyboardButton(i18n.get('best_quality'), callback_data='format_best')],
        [InlineKeyboardButton(i18n.get('audio_only'), callback_data='format_audio')],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = i18n.get('video_title', title=title) + "\n\n" + i18n.get('select_format', formats='')
    
    await processing_msg.edit_text(message_text, reply_markup=reply_markup)


async def handle_format_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle format selection from inline keyboard"""
    query = update.callback_query
    await query.answer()
    
    url = context.user_data.get('last_url')
    
    if not url:
        await query.edit_message_text(i18n.get('no_url_saved'))
        return
    
    # Update message to show downloading status
    await query.edit_message_text(i18n.get('downloading'))
    
    # Determine which format to download
    format_choice = query.data
    
    try:
        if format_choice == 'format_best':
            filepath = downloader.download_best(url)
        elif format_choice == 'format_audio':
            filepath = downloader.download_audio(url)
        else:
            await query.edit_message_text(i18n.get('invalid_format'))
            return
        
        if not filepath:
            await query.edit_message_text(i18n.get('file_too_large'))
            return
        
        # Upload file to Telegram
        await query.edit_message_text(i18n.get('uploading'))
        
        # Send file based on type
        if filepath.endswith('.mp3'):
            with open(filepath, 'rb') as audio_file:
                await context.bot.send_audio(
                    chat_id=query.message.chat_id,
                    audio=audio_file,
                    title=context.user_data.get('video_title', 'Audio')
                )
        else:
            with open(filepath, 'rb') as video_file:
                await context.bot.send_video(
                    chat_id=query.message.chat_id,
                    video=video_file,
                    caption=context.user_data.get('video_title', '')
                )
        
        # Delete the processing message and send success message
        await query.message.delete()
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=i18n.get('download_complete')
        )
        
        # Cleanup
        downloader.cleanup_file(filepath)
        
    except Exception as e:
        await query.edit_message_text(i18n.get('error_occurred', error=str(e)))
        if 'filepath' in locals() and filepath:
            downloader.cleanup_file(filepath)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages"""
    text = update.message.text
    
    # Check if it's a URL
    if text.startswith('http://') or text.startswith('https://'):
        await handle_url(update, context)
    else:
        await update.message.reply_text(i18n.get('send_link'))