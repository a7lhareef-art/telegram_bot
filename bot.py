import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ========== توكن البوت (من متغيرات البيئة) ==========
TOKEN = os.environ.get("BOT_TOKEN", "8853272940:AAFnbQLN3-QcHeJa9_gMx-s7Xa8BncfrsVM")

# ========== البيانات المؤقتة ==========
user_data = {
    "points": 1,
    "user_id": 8811384711,
    "completed_orders": 1234
}

# ========== لوحة المفاتيح الرئيسية ==========
def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🟢 خدمات مدفوعة", callback_data='paid_services')],
        [InlineKeyboardButton("🟢 مجانية", callback_data='free_services')],
        [InlineKeyboardButton("💰 عدد نقاطي", callback_data='my_points')],
        [InlineKeyboardButton("🆔 معرفي", callback_data='my_id')],
        [InlineKeyboardButton("⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯", callback_data='dummy')],
        [InlineKeyboardButton("📌 خدمات الرشق", callback_data='rash_services')],
        [InlineKeyboardButton("📌 طلباتي", callback_data='my_orders')],
        [InlineKeyboardButton("📌 فحص طلب", callback_data='check_order')],
        [InlineKeyboardButton("📌 معلومات الحساب", callback_data='account_info')],
        [InlineKeyboardButton("📌 شحن نقاط", callback_data='charge_points')],
        [InlineKeyboardButton("📌 قناة البوت", callback_data='bot_channel')],
        [InlineKeyboardButton("📌 شروط الاستخدام", callback_data='terms')],
    ]
    return InlineKeyboardMarkup(keyboard)

# ========== قائمة خدمات الرشق ==========
def rash_services_keyboard():
    keyboard = [
        [InlineKeyboardButton("🎁 خدمات مجانية", callback_data='free_services')],
        [InlineKeyboardButton("💳 خدمات مدفوعة", callback_data='paid_services_rash')],
        [InlineKeyboardButton("🔙 رجوع", callback_data='back_to_main')],
    ]
    return InlineKeyboardMarkup(keyboard)

# ========== زر الرجوع ==========
def back_button():
    keyboard = [[InlineKeyboardButton("🔙 رجوع", callback_data='back_to_main')]]
    return InlineKeyboardMarkup(keyboard)

# ========== أمر /start ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = f"""
<b>👋 مرحبا بك في بوت الخدمات الشامل</b>
<i>أفضل بوت خدمات "الاختيار المناسب لك"</i>

<code>🟢 خدمات مدفوعة</code>
<code>🟢 مجانية</code>

💰 <b>عدد نقاط:</b> <code>{user_data['points']}</code>
🆔 <b>ايديك:</b> <code>{user_data['user_id']}</code>

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯

✅ <b>طلبات مكتملة:</b> <code>{user_data['completed_orders']}</code>
    """
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=main_menu_keyboard(),
        parse_mode='HTML'
    )

# ========== معالجة الأزرار ==========
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'back_to_main':
        await start(update, context)
        return

    if data == 'rash_services':
        await query.edit_message_text(
            "<b>📌 خدمات الرشق</b>\n\nاختر نوع الخدمة:",
            reply_markup=rash_services_keyboard(),
            parse_mode='HTML'
        )
        return

    if data == 'free_services':
        await query.edit_message_text(
            """
<b>🎁 الخدمات المجانية</b>

━━━━━━━━━━━━━━━━━━━
<b>📱 تيلجرام</b>
━━━━━━━━━━━━━━━━━━━
🎁 <code>تفاعل بوست تيلجرام [ 👍 ] مع مشاهدات مجاناً</code>
🎁 <code>تفاعل بوست تيلجرام [ 👎 ] مع مشاهدات مجاناً</code>
🎁 <code>تفاعل بوست تيلجرام [ ❤️ ] مع مشاهدات مجاناً</code>
🎁 <code>تفاعل بوست تيلجرام [ 🔥 ] مع مشاهدات مجاناً</code>
🎁 <code>تفاعل بوست تيلجرام [ 🥰 ] مع مشاهدات مجاناً</code>
🎁 <code>تفاعل بوست تيلجرام [ 😍 ] مع مشاهدات مجاناً</code>
🎁 <code>تفاعل بوست تيلجرام [ 👏 ] مع مشاهدات مجاناً</code>
🎁 <code>تفاعل بوست تيلجرام [ 😁 ] مع مشاهدات مجاناً</code>
🎁 <code>تفاعل بوست تيلجرام [ 🤔 ] مع مشاهدات مجاناً</code>
🎁 <code>تفاعل بوست تيلجرام [ 🤠 ] مع مشاهدات مجاناً</code>
🎁 <code>تفاعل بوست تيلجرام [ 😱 ] مع مشاهدات مجاناً</code>
🎁 <code>تفاعل بوست تيلجرام [ 🐳 ] مع مشاهدات مجاناً</code>
🎁 <code>تفاعل بوست تيلجرام [ 🥵 ] مع مشاهدات مجاناً</code>
🎁 <code>تفاعل بوست تيلجرام [ 😢 ] مع مشاهدات مجاناً</code>
🎁 <code>تفاعل بوست تيلجرام [ 🎉 ] مع مشاهدات مجاناً</code>
🎁 <code>تفاعل بوست تيلجرام [ 😂 ] مع مشاهدات مجاناً</code>
🎁 <code>تفاعل بوست تيلجرام [ 🤢 ] مع مشاهدات مجاناً</code>
🎁 <code>تفاعل بوست تيلجرام [ 💩 ] مع مشاهدات مجاناً</code>
🎁 <code>تفاعل بوست تيلجرام [ 🙏 ] مع مشاهدات مجاناً</code>
🎁 <code>تفاعل بوست تيلجرام [ 👌 ] مع مشاهدات مجاناً</code>
🎁 <code>تفاعل بوست تيلجرام [ 🕊️ ] مع مشاهدات مجاناً</code>
🎁 <code>تفاعل بوست تيلجرام [ 🤡 ] مع مشاهدات مجاناً</code>
🎁 <code>تفاعل بوست تيلجرام [ 😘 ] مع مشاهدات مجاناً</code>
✅ <code>مشتركين قناة تيلجرام مجاناً</code>

━━━━━━━━━━━━━━━━━━━
<b>🎵 تيك توك</b>
━━━━━━━━━━━━━━━━━━━
✅ <code>تفاصيل تيك توك مجاناً</code>
✅ <code>تكتيبات بث مباشر تيك توك مجاناً</code>
✅ <code>مشاهدات فيديو تيك توك مجاناً</code>
✅ <code>اليكات فيديو تيك توك مجاناً</code>

━━━━━━━━━━━━━━━━━━━
<b>📷 إنستغرام</b>
━━━━━━━━━━━━━━━━━━━
✅ <code>متابعين إنستغرام مجاناً</code>
✅ <code>اليكات إنستغرام مجاناً</code>
✅ <code>تعليقات منشور إنستغرام عشوائية مجاناً</code>
✅ <code>مشاهدات فيديو إنستغرام مجاناً</code>
✅ <code>حفظ منشور إنستغرام مجاناً</code>
✅ <code>اليكات تعليقات إنستغرام مجاناً</code>
✅ <code>إعادة نشر منشور إنستغرام مجاناً</code>
✅ <code>مشاركات منشور إنستغرام مجاناً</code>

━━━━━━━━━━━━━━━━━━━
<b>▶️ يوتيوب</b>
━━━━━━━━━━━━━━━━━━━
✅ <code>مشتركين قناة يوتيوب مجاناً</code>
✅ <code>اليكات فيديو يوتيوب مجاناً</code>

━━━━━━━━━━━━━━━━━━━
<b>📘 فيسبوك</b>
━━━━━━━━━━━━━━━━━━━
✅ <code>متابعين فيسبوك مجاناً</code>
✅ <code>اليكات منشور فيسبوك مجاناً</code>
✅ <code>اليكات فيديو فيسبوك مجاناً</code>

━━━━━━━━━━━━━━━━━━━
<b>🐦 تويتر (X)</b>
━━━━━━━━━━━━━━━━━━━
✅ <code>متابعين تويتر مجاناً</code>
✅ <code>اليكات منشور تويتر مجاناً</code>

━━━━━━━━━━━━━━━━━━━
<b>🎬 كوآي</b>
━━━━━━━━━━━━━━━━━━━
✅ <code>متابعين كوآي مجاناً</code>
✅ <code>اليكات فيديو كوآي مجاناً</code>
✅ <code>اليكات منشور كوآي مجاناً</code>
            """,
            reply_markup=back_button(),
            parse_mode='HTML'
        )
        return

    if data == 'paid_services_rash' or data == 'paid_services':
        await query.edit_message_text(
            """
<b>💳 الخدمات المدفوعة</b>

🔹 <b>الخدمة 1:</b> <code>شرح الخدمة</code>
🔹 <b>الخدمة 2:</b> <code>شرح الخدمة</code>
🔹 <b>الخدمة 3:</b> <code>شرح الخدمة</code>

💰 <b>السعر:</b> <code>5 نقاط</code>
            """,
            reply_markup=back_button(),
            parse_mode='HTML'
        )
        return

    if data == 'my_points':
        await query.edit_message_text(
            f"""
💰 <b>نقاطك الحالية</b>

<code>{user_data['points']}</code> نقطة
            """,
            reply_markup=back_button(),
            parse_mode='HTML'
        )
        return

    if data == 'my_id':
        await query.edit_message_text(
            f"""
🆔 <b>معرفك</b>

<code>{user_data['user_id']}</code>
            """,
            reply_markup=back_button(),
            parse_mode='HTML'
        )
        return

    if data == 'my_orders':
        await query.edit_message_text(
            """
<b>📋 طلباتي</b>

📌 <b>طلب 1:</b> <code>قيد التنفيذ</code>
✅ <b>طلب 2:</b> <code>مكتمل</code>
⏳ <b>طلب 3:</b> <code>قيد المراجعة</code>
            """,
            reply_markup=back_button(),
            parse_mode='HTML'
        )
        return

    if data == 'check_order':
        await query.edit_message_text(
            """
<b>🔍 فحص طلب</b>

📝 أرسل رقم الطلب للتحقق من حالته
            """,
            reply_markup=back_button(),
            parse_mode='HTML'
        )
        return

    if data == 'account_info':
        await query.edit_message_text(
            f"""
<b>👤 معلومات الحساب</b>

🆔 <b>المعرف:</b> <code>{user_data['user_id']}</code>
💰 <b>النقاط:</b> <code>{user_data['points']}</code>
✅ <b>الطلبات المكتملة:</b> <code>{user_data['completed_orders']}</code>
            """,
            reply_markup=back_button(),
            parse_mode='HTML'
        )
        return

    if data == 'charge_points':
        await query.edit_message_text(
            """
<b>💳 شحن نقاط</b>

📞 للشحن تواصل مع المطور:
👤 <a href='https://t.me/YourUsername'>@YourUsername</a>
            """,
            reply_markup=back_button(),
            parse_mode='HTML'
        )
        return

    if data == 'bot_channel':
        await query.edit_message_text(
            """
<b>📢 قناة البوت</b>

🔗 <a href='https://t.me/YourChannelLink'>اضغط هنا للانضمام</a>
            """,
            reply_markup=back_button(),
            parse_mode='HTML'
        )
        return

    if data == 'terms':
        await query.edit_message_text(
            """
<b>📜 شروط الاستخدام</b>

1️⃣ <code>الالتزام بالقوانين</code>
2️⃣ <code>عدم استخدام البوت في التزوير</code>
3️⃣ <code>حقوق النشر محفوظة</code>
            """,
            reply_markup=back_button(),
            parse_mode='HTML'
        )
        return

    if data == 'dummy':
        await query.edit_message_text(
            "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
            reply_markup=back_button(),
            parse_mode='HTML'
        )
        return

    await query.edit_message_text("⚠️ زر غير معروف")

# ========== تشغيل البوت ==========
def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("🚀 البوت يعمل...")
    app.run_polling()

if __name__ == "__main__":
    main()
