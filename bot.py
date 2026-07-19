import os
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.request import HTTPXRequest

TOKEN = os.environ.get("BOT_TOKEN", "8853272940:AAFnbQLN3-QcHeJa9_gMx-s7Xa8BncfrsVM")

# ========== إعدادات الاتصال ==========
request = HTTPXRequest(
    connect_timeout=30.0,
    read_timeout=30.0,
)

# ========== بيانات المستخدم ==========
user_data = {
    "points": 0,
    "join_time": None
}

# ========== القائمة الرئيسية ==========
def main_menu():
    keyboard = [
        [InlineKeyboardButton("🟢 شراء أرقام", callback_data='buy_numbers')],
        [InlineKeyboardButton("🔴 خدمات الرشق", callback_data='rash_services')],
        [InlineKeyboardButton("🟡 شحن الرصيد", callback_data='charge_balance')],
        [InlineKeyboardButton("🔵 معلوماتي", callback_data='my_info')],
        [InlineKeyboardButton("🟣 الدعم", callback_data='support')],
    ]
    return InlineKeyboardMarkup(keyboard)

# ========== قائمة شراء أرقام ==========
def buy_numbers_menu():
    keyboard = [
        [InlineKeyboardButton("📱 أرقام تليجرام", callback_data='buy_telegram')],
        [InlineKeyboardButton("💬 أرقام واتساب", callback_data='buy_whatsapp')],
        [InlineKeyboardButton("🔙 رجوع", callback_data='back_main')],
    ]
    return InlineKeyboardMarkup(keyboard)

# ========== قائمة خدمات الرشق ==========
def rash_services_menu():
    keyboard = [
        [InlineKeyboardButton("🎵 TikTok", callback_data='rash_tiktok')],
        [InlineKeyboardButton("📷 Instagram", callback_data='rash_instagram')],
        [InlineKeyboardButton("▶️ YouTube", callback_data='rash_youtube')],
        [InlineKeyboardButton("📘 Facebook", callback_data='rash_facebook')],
        [InlineKeyboardButton("🐦 Twitter", callback_data='rash_twitter')],
        [InlineKeyboardButton("🎬 Kwai", callback_data='rash_kwai')],
        [InlineKeyboardButton("📺 Twitch", callback_data='rash_twitch')],
        [InlineKeyboardButton("🔙 رجوع", callback_data='back_main')],
    ]
    return InlineKeyboardMarkup(keyboard)

# ========== قائمة شحن الرصيد ==========
def charge_menu():
    keyboard = [
        [InlineKeyboardButton("💳 فودافون كاش", callback_data='charge_vodafone')],
        [InlineKeyboardButton("🏦 إنستا باي", callback_data='charge_instapay')],
        [InlineKeyboardButton("💵 باي بال", callback_data='charge_paypal')],
        [InlineKeyboardButton("🔙 رجوع", callback_data='back_main')],
    ]
    return InlineKeyboardMarkup(keyboard)

# ========== زر الرجوع ==========
def back_button():
    keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data='back_main')]]
    return InlineKeyboardMarkup(keyboard)

# ========== أمر /start ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    if user_data["join_time"] is None:
        user_data["join_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    welcome_text = f"""
🚀 **مرحباً بك في بوت الخدمات الشامل!**

👤 {user.full_name}
🆔 {user.id}

📌 اختر الخدمة المناسبة من الأزرار أدناه 👇
    """
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=main_menu(),
        parse_mode='Markdown'
    )

# ========== معالجة الأزرار ==========
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user = update.effective_user

    if data == 'back_main':
        await start(update, context)
        return

    if data == 'buy_numbers':
        await query.edit_message_text(
            "📱 **شراء أرقام**\n\nاختر نوع الرقم:",
            reply_markup=buy_numbers_menu(),
            parse_mode='Markdown'
        )
        return

    if data == 'buy_telegram':
        await query.edit_message_text(
            "📱 **شراء أرقام تليجرام**\n\n💰 السعر: 5 نقاط\n\n📤 أرسل الكمية المطلوبة:",
            reply_markup=back_button(),
            parse_mode='Markdown'
        )
        return

    if data == 'buy_whatsapp':
        await query.edit_message_text(
            "💬 **شراء أرقام واتساب**\n\n💰 السعر: 3 نقاط\n\n📤 أرسل الكمية المطلوبة:",
            reply_markup=back_button(),
            parse_mode='Markdown'
        )
        return

    if data == 'rash_services':
        await query.edit_message_text(
            "🔴 **خدمات الرشق**\n\nاختر المنصة:",
            reply_markup=rash_services_menu(),
            parse_mode='Markdown'
        )
        return

    rash_services_list = {
        'rash_tiktok': '🎵 TikTok',
        'rash_instagram': '📷 Instagram',
        'rash_youtube': '▶️ YouTube',
        'rash_facebook': '📘 Facebook',
        'rash_twitter': '🐦 Twitter',
        'rash_kwai': '🎬 Kwai',
        'rash_twitch': '📺 Twitch'
    }
    
    if data in rash_services_list:
        service_name = rash_services_list[data]
        await query.edit_message_text(
            f"✅ **{service_name}**\n\n📤 أرسل رابط المنشور/الفيديو الآن:",
            reply_markup=back_button(),
            parse_mode='Markdown'
        )
        return

    if data == 'charge_balance':
        await query.edit_message_text(
            "🟡 **شحن الرصيد**\n\nاختر طريقة الدفع:",
            reply_markup=charge_menu(),
            parse_mode='Markdown'
        )
        return

    charge_methods = {
        'charge_vodafone': '💳 فودافون كاش',
        'charge_instapay': '🏦 إنستا باي',
        'charge_paypal': '💵 باي بال'
    }
    
    if data in charge_methods:
        method_name = charge_methods[data]
        await query.edit_message_text(
            f"✅ **طريقة الدفع: {method_name}**\n\n"
            f"📞 رقم التحويل: 0123456789\n"
            f"🏷️ الاسم: أحمد محمد\n\n"
            f"📤 أرسل صورة الإيصال بعد التحويل:",
            reply_markup=back_button(),
            parse_mode='Markdown'
        )
        return

    if data == 'my_info':
        join_time = user_data["join_time"] or "غير مسجل"
        await query.edit_message_text(
            f"""
🔵 **معلوماتي**

👤 الاسم: {user.full_name}
🆔 اليوزر: @{user.username if user.username else 'لا يوجد'}
🆔 الأيدي: {user.id}
📅 وقت الدخول: {join_time}
💰 الرصيد: {user_data['points']} نقطة
            """,
            reply_markup=back_button(),
            parse_mode='Markdown'
        )
        return

    if data == 'support':
        await query.edit_message_text(
            """
🟣 **الدعم الفني**

للتواصل مع فريق الدعم:

👤 @YourSupportUsername

📩 أو أرسل رسالتك وسنرد عليك في أقرب وقت!
            """,
            reply_markup=back_button(),
            parse_mode='Markdown'
        )
        return

    await query.edit_message_text("⚠️ زر غير معروف")

# ========== أمر مساعدة ==========
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📖 **مساعدة البوت**

🔹 /start - عرض القائمة الرئيسية
🔹 /help - عرض هذه الرسالة

📌 **الخدمات المتاحة:**
• شراء أرقام (تليجرام - واتساب)
• خدمات الرشق (TikTok - Instagram - YouTube - Facebook - Twitter - Kwai - Twitch)
• شحن الرصيد
• معلوماتي
• الدعم الفني
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

# ========== تشغيل البوت ==========
def main():
    app = Application.builder().token(TOKEN).request(request).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("🚀 البوت يعمل...")
    app.run_polling()

if __name__ == "__main__":
    main()
