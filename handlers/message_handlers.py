from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatMember
from telegram.ext import ContextTypes
from telegram.error import BadRequest
from utils.localization import i18n
from utils.downloader import VideoDownloader
from config.settings import REQUIRED_CHANNELS
import os


# Initialize downloader
downloader = VideoDownloader()


async def check_channel_membership(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """
    Check if user is member of required channels
    
    Returns:
        True if user is member of all required channels or no channels required
        False if user is not member
    """
    if not REQUIRED_CHANNELS:
        return True
    
    user_id = update.effective_user.id
    not_joined_channels = []
    
    for channel in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status in [ChatMember.LEFT, ChatMember.BANNED]:
                not_joined_channels.append(channel)
        except BadRequest:
            # Channel might not exist or bot is not admin
            print(f"Error checking membership for channel: {channel}")
            continue
    
    if not_joined_channels:
        # Create join buttons for channels user hasn't joined
        keyboard = []
        for channel in not_joined_channels:
            # Remove @ if present to create proper link
            channel_username = channel.replace('@', '')
            keyboard.append([InlineKeyboardButton(
                f"🔗 عضویت در {channel}",
                url=f"https://t.me/{channel_username}"
            )])
        
        # Add check membership button
        keyboard.append([InlineKeyboardButton("✅ عضو شدم، بررسی کن", callback_data='check_membership')])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = i18n.get('join_channels')
        
        if update.callback_query:
            await update.callback_query.answer(i18n.get('not_member_alert'), show_alert=True)
            await update.callback_query.message.reply_text(message, reply_markup=reply_markup)
        else:
            await update.message.reply_text(message, reply_markup=reply_markup)
        
        return False
    
    return True


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    # Check channel membership
    if not await check_channel_membership(update, context):
        return
    
    await update.message.reply_text(i18n.get('welcome'))


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    # Check channel membership
    if not await check_channel_membership(update, context):
        return
    
    await update.message.reply_text(i18n.get('help'))


async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /cancel command"""
    # Clear user data
    context.user_data.clear()
    await update.message.reply_text(i18n.get('operation_cancelled'))


async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming URLs with inline quality selection"""
    # Check channel membership
    if not await check_channel_membership(update, context):
        return
    
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
    
    # Get video title and duration
    title = info.get('title', 'Unknown')
    duration = info.get('duration', 0)
    context.user_data['video_title'] = title
    
    # Format duration
    duration_str = ""
    if duration:
        minutes = duration // 60
        seconds = duration % 60
        duration_str = f"\n⏱ مدت زمان: {minutes}:{seconds:02d}"
    
    # Create quality selection buttons (inline keyboard)
    keyboard = [
        [InlineKeyboardButton("🌟 بهترین کیفیت", callback_data='quality_best')],
        [InlineKeyboardButton("📺 کیفیت متوسط (720p)", callback_data='quality_medium')],
        [InlineKeyboardButton("📱 کیفیت پایین (360p)", callback_data='quality_low')],
        [InlineKeyboardButton("🎵 فقط صدا (MP3)", callback_data='quality_audio')],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    message_text = f"📹 {title}{duration_str}\n\n{i18n.get('select_format', formats='')}"
    
    await processing_msg.edit_text(message_text, reply_markup=reply_markup)


async def handle_quality_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle quality selection from inline keyboard"""
    query = update.callback_query
    
    # Check if this is the membership check callback
    if query.data == 'check_membership':
        await query.answer()
        # Re-check membership
        if await check_channel_membership(update, context):
            await query.message.edit_text(i18n.get('membership_verified'))
        return
    
    await query.answer()
    
    url = context.user_data.get('last_url')
    
    if not url:
        await query.edit_message_text(i18n.get('no_url_saved'))
        return
    
    # Update message to show downloading status
    await query.edit_message_text(i18n.get('downloading'))
    
    # Determine which quality to download
    quality_choice = query.data
    
    try:
        if quality_choice == 'quality_best':
            filepath = downloader.download_best(url)
        elif quality_choice == 'quality_medium':
            filepath = downloader.download_medium(url)
        elif quality_choice == 'quality_low':
            filepath = downloader.download_low(url)
        elif quality_choice == 'quality_audio':
            filepath = downloader.download_audio(url)
        else:
            await query.edit_message_text(i18n.get('invalid_format'))
            return
        
        if not filepath:
            await query.edit_message_text(i18n.get('file_too_large'))
            return
        
        # Check if file exists and get size
        if not os.path.exists(filepath):
            await query.edit_message_text(i18n.get('error_occurred', error='فایل دانلود نشد'))
            return
        
        file_size = os.path.getsize(filepath)
        file_size_mb = file_size / (1024 * 1024)
        
        # Upload file to Telegram
        await query.edit_message_text(i18n.get('uploading'))
        
        # Send file based on type
        if filepath.endswith('.mp3'):
            with open(filepath, 'rb') as audio_file:
                await context.bot.send_audio(
                    chat_id=query.message.chat_id,
                    audio=audio_file,
                    title=context.user_data.get('video_title', 'Audio'),
                    caption=f"🎵 {context.user_data.get('video_title', '')}\n\n📦 حجم: {file_size_mb:.1f} MB"
                )
        else:
            with open(filepath, 'rb') as video_file:
                # Send as video with proper width/height to preserve aspect ratio
                await context.bot.send_video(
                    chat_id=query.message.chat_id,
                    video=video_file,
                    caption=f"📹 {context.user_data.get('video_title', '')}\n\n📦 حجم: {file_size_mb:.1f} MB",
                    supports_streaming=True,
                    width=None,  # Let Telegram detect
                    height=None  # Let Telegram detect
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
        error_msg = str(e)
        if "file is too big" in error_msg.lower():
            await query.edit_message_text(i18n.get('file_too_large'))
        else:
            await query.edit_message_text(i18n.get('error_occurred', error=error_msg))
        
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