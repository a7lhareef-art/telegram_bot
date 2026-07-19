import os
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN", "8853272940:AAFnbQLN3-QcHeJa9_gMx-s7Xa8BncfrsVM")

user_data = {
    "points": 0,
    "join_time": None
}

# القائمة الرئيسية
def main_menu():
    keyboard = [
        [InlineKeyboardButton("🟢 شراء أرقام", callback_data='buy_numbers')],
        [InlineKeyboardButton("🔴 خدمات الرشق", callback_data='rash_services')],
        [InlineKeyboardButton("🟡 شحن الرصيد", callback_data='charge_balance')],
        [InlineKeyboardButton("🔵 معلوماتي", callback_data='my_info')],
        [InlineKeyboardButton("🟣 الدعم", callback_data='support')],
    ]
    return InlineKeyboardMarkup(keyboard)

# قائمة شراء أرقام
def buy_numbers_menu():
    keyboard = [
        [InlineKeyboardButton("📱 أرقام تليجرام", callback_data='buy_telegram')],
        [InlineKeyboardButton("💬 أرقام واتساب", callback_data='buy_whatsapp')],
        [InlineKeyboardButton("🔙 رجوع", callback_data='back_main')],
    ]
    return InlineKeyboardMarkup(keyboard)

# قائمة خدمات الرشق
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

# قائمة شحن الرصيد
def charge_menu():
    keyboard = [
        [InlineKeyboardButton("💳 فودافون كاش", callback_data='charge_vodafone')],
        [InlineKeyboardButton("🏦 إنستا باي", callback_data='charge_instapay')],
        [InlineKeyboardButton("💵 باي بال", callback_data='charge_paypal')],
        [InlineKeyboardButton("🔙 رجوع", callback_data='back_main')],
    ]
    return InlineKeyboardMarkup(keyboard)

def back_button():
    keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data='back_main')]]
    return InlineKeyboardMarkup(keyboard)

# أمر start
async def start(update, context):
    user = update.effective_user
    if user_data["join_time"] is None:
        user_data["join_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    text = f"🚀 مرحباً بك في بوت الخدمات الشامل!\n\n👤 {user.full_name}\n🆔 {user.id}\n\n📌 اختر الخدمة:"
    await update.message.reply_text(text, reply_markup=main_menu())

# معالجة الأزرار
async def button_handler(update, context):
    query = update.callback_query
    await query.answer()
    data = query.data
    user = update.effective_user

    if data == 'back_main':
        await start(update, context)
        return

    if data == 'buy_numbers':
        await query.edit_message_text("📱 شراء أرقام\n\nاختر نوع الرقم:", reply_markup=buy_numbers_menu())
        return

    if data == 'buy_telegram':
        await query.edit_message_text("📱 شراء أرقام تليجرام\n💰 السعر: 5 نقاط\n\n📤 أرسل الكمية:", reply_markup=back_button())
        return

    if data == 'buy_whatsapp':
        await query.edit_message_text("💬 شراء أرقام واتساب\n💰 السعر: 3 نقاط\n\n📤 أرسل الكمية:", reply_markup=back_button())
        return

    if data == 'rash_services':
        await query.edit_message_text("🔴 خدمات الرشق\n\nاختر المنصة:", reply_markup=rash_services_menu())
        return

    if data in ['rash_tiktok', 'rash_instagram', 'rash_youtube', 'rash_facebook', 'rash_twitter', 'rash_kwai', 'rash_twitch']:
        names = {
            'rash_tiktok': 'TikTok', 'rash_instagram': 'Instagram',
            'rash_youtube': 'YouTube', 'rash_facebook': 'Facebook',
            'rash_twitter': 'Twitter', 'rash_kwai': 'Kwai', 'rash_twitch': 'Twitch'
        }
        await query.edit_message_text(f"✅ {names[data]}\n\n📤 أرسل الرابط:", reply_markup=back_button())
        return

    if data == 'charge_balance':
        await query.edit_message_text("🟡 شحن الرصيد\n\nاختر طريقة الدفع:", reply_markup=charge_menu())
        return

    if data in ['charge_vodafone', 'charge_instapay', 'charge_paypal']:
        names = {'charge_vodafone': 'فودافون كاش', 'charge_instapay': 'إنستا باي', 'charge_paypal': 'باي بال'}
        await query.edit_message_text(
            f"✅ طريقة الدفع: {names[data]}\n\n📞 رقم التحويل: 0123456789\n🏷️ الاسم: أحمد محمد\n\n📤 أرسل صورة الإيصال:",
            reply_markup=back_button()
        )
        return

    if data == 'my_info':
        join_time = user_data["join_time"] or "غير مسجل"
        text = f"🔵 معلوماتي\n\n👤 الاسم: {user.full_name}\n🆔 اليوزر: @{user.username if user.username else 'لا يوجد'}\n🆔 الأيدي: {user.id}\n📅 وقت الدخول: {join_time}\n💰 الرصيد: {user_data['points']} نقطة"
        await query.edit_message_text(text, reply_markup=back_button())
        return

    if data == 'support':
        await query.edit_message_text("🟣 الدعم الفني\n\nللتواصل: @YourSupportUsername", reply_markup=back_button())
        return

    await query.edit_message_text("⚠️ زر غير معروف")

# أمر مساعدة
async def help_command(update, context):
    text = "📖 مساعدة البوت\n\n/start - القائمة الرئيسية\n/help - هذه الرسالة"
    await update.message.reply_text(text)

# تشغيل البوت
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("🚀 البوت شغال...")
    app.run_polling()

if __name__ == "__main__":
    main()
