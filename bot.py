import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ==========================================
# 1. التوكن من البيئة (Variables)
# ==========================================
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN مش موجود في متغيرات البيئة!")

# ==========================================
# 2. أمر /start (للاختبار)
# ==========================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ البوت شغال! \n\nقريباً هتضاف كل الأقسام.")

# ==========================================
# 3. التشغيل
# ==========================================
def main():
    logging.basicConfig(level=logging.INFO)
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("✅ البوت شغال...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
