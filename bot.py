import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

print("🚀 جاري تشغيل البوت...")

# ==========================================
# جلب التوكن من البيئة مع تأكيد
# ==========================================
BOT_TOKEN = os.environ.get("BOT_TOKEN")

print(f"🔑 هل التوكن موجود؟ {'✅ نعم' if BOT_TOKEN else '❌ لا'}")
if BOT_TOKEN:
    print(f"🔑 أول 5 حروف من التوكن: {BOT_TOKEN[:5]}...")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN مش موجود في متغيرات البيئة!")

# ==========================================
# أمر /start
# ==========================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ البوت شغال! \n\nجهز نفسك لباقي الأقسام.")

# ==========================================
# التشغيل
# ==========================================
def main():
    logging.basicConfig(level=logging.INFO)
    print("🛠 جاري بناء التطبيق...")
    app = Application.builder().token(BOT_TOKEN).build()
    print("🏗 تم بناء التطبيق بنجاح.")
    app.add_handler(CommandHandler("start", start))
    
    print("✅ البوت شغال...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
