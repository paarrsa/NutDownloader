# Adding New Languages Guide

## How to Add a New Language

### Step 1: Create Language File

Create a new JSON file in the `locales/` directory with the language code:

```bash
# For Arabic
nano locales/ar.json

# For French
nano locales/fr.json

# For Spanish
nano locales/es.json
```

### Step 2: Copy Template

Use this template and translate all strings:

```json
{
  "welcome": "Your translation here",
  "help": "Your translation here",
  "send_link": "Your translation here",
  "processing": "Your translation here",
  "extracting_info": "Your translation here",
  "downloading": "Your translation here",
  "uploading": "Your translation here",
  "download_complete": "Your translation here",
  "error_occurred": "Your translation here (use {error} placeholder)",
  "invalid_url": "Your translation here",
  "file_too_large": "Your translation here",
  "no_url_saved": "Your translation here",
  "formats_available": "Your translation here (use {formats} placeholder)",
  "select_format": "Your translation here (use {formats} placeholder)",
  "invalid_format": "Your translation here",
  "operation_cancelled": "Your translation here",
  "downloading_progress": "Your translation here (use {percent} placeholder)",
  "best_quality": "Your translation here",
  "audio_only": "Your translation here",
  "video_title": "Your translation here (use {title} placeholder)",
  "unsupported_site": "Your translation here"
}
```

### Step 3: Test the New Language

1. Change default language in `config/settings.py`:
```python
DEFAULT_LANGUAGE = 'ar'  # Your new language code
```

2. Restart the bot:
```bash
sudo systemctl restart telegram-bot.service
```

## Example: Adding Arabic

Create `locales/ar.json`:
```json
{
  "welcome": "مرحبا! 👋\n\nأنا روبوت تنزيل الفيديو. يمكنني تنزيل مقاطع الفيديو من أكثر من 1000 موقع!\n\n🎬 فقط أرسل لي رابط الفيديو.\n\n📝 الأوامر:\n/start - بدء الروبوت\n/help - المساعدة\n/formats - عرض التنسيقات المتاحة\n/cancel - إلغاء العملية",
  "help": "📖 كيفية الاستخدام:\n\n1️⃣ أرسل رابط الفيديو\n2️⃣ اختر التنسيق المفضل\n3️⃣ انتظر التنزيل\n\n✨ المواقع المدعومة:\n• يوتيوب\n• إنستغرام\n• تويتر\n• تيك توك\n• وأكثر من 1000 موقع آخر!",
  "send_link": "الرجاء إرسال رابط الفيديو:",
  "processing": "⏳ جاري المعالجة...",
  "extracting_info": "🔍 جاري استخراج المعلومات...",
  "downloading": "⬇️ جاري التنزيل...\n\nقد يستغرق هذا بضع دقائق.",
  "uploading": "⬆️ جاري الرفع إلى تيليجرام...",
  "download_complete": "✅ اكتمل التنزيل بنجاح!",
  "error_occurred": "❌ حدث خطأ:\n\n{error}",
  "invalid_url": "❌ رابط غير صالح. الرجاء إرسال رابط صحيح.",
  "file_too_large": "❌ الملف كبير جداً (الحد الأقصى 50 ميجابايت).\n\nالرجاء اختيار تنسيق بجودة أقل.",
  "no_url_saved": "❌ لا يوجد رابط محفوظ. الرجاء إرسال رابط أولاً.",
  "formats_available": "📋 التنسيقات المتاحة:\n\n{formats}\n\nللتنزيل، أرسل رقم التنسيق",
  "select_format": "الرجاء اختيار التنسيق المفضل:\n\n{formats}",
  "invalid_format": "❌ تنسيق غير صالح. الرجاء الاختيار من الأزرار.",
  "operation_cancelled": "❌ تم إلغاء العملية.",
  "downloading_progress": "⬇️ جاري التنزيل... {percent}%",
  "best_quality": "🌟 أفضل جودة",
  "audio_only": "🎵 صوت فقط",
  "video_title": "📹 العنوان: {title}",
  "unsupported_site": "❌ هذا الموقع غير مدعوم أو الرابط غير صالح."
}
```

## Dynamic Language Selection (Advanced)

To allow users to choose their language dynamically, you can:

1. Add a language selection command in `handlers/message_handlers.py`
2. Store user language preference in user_data
3. Pass the language to i18n.get() calls

Example:
```python
async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /language command"""
    keyboard = [
        [InlineKeyboardButton("🇮🇷 فارسی", callback_data='lang_fa')],
        [InlineKeyboardButton("🇬🇧 English", callback_data='lang_en')],
        [InlineKeyboardButton("🇸🇦 العربية", callback_data='lang_ar')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select language:", reply_markup=reply_markup)

async def handle_language_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle language selection"""
    query = update.callback_query
    await query.answer()
    
    lang = query.data.replace('lang_', '')
    context.user_data['language'] = lang
    
    await query.edit_message_text(i18n.get('welcome', lang=lang))
```

Then use in handlers:
```python
# Get user's preferred language
user_lang = context.user_data.get('language', 'fa')
await update.message.reply_text(i18n.get('processing', lang=user_lang))
```

## Available Language Codes

- `fa` - Persian (فارسی)
- `en` - English
- `ar` - Arabic (العربية)
- `fr` - French (Français)
- `es` - Spanish (Español)
- `de` - German (Deutsch)
- `ru` - Russian (Русский)
- `tr` - Turkish (Türkçe)
- `zh` - Chinese (中文)

Use ISO 639-1 language codes for consistency.