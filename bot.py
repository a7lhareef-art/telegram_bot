import os
import logging
import sqlite3
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# ======================================================
# 1. الإعدادات (التوكن هيجيلك من البيئة)
# ======================================================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN مش موجود في متغيرات البيئة!")

ADMIN_ID = 8933825471
SHOP_NAME = "PrimeX Store | برايم إكس ستور"
SUPPORT_USERNAME = "@PrimeXStore22"
SUPPORT_LINK = "https://t.me/PrimeXStore22"

# ======================================================
# 2. قاعدة البيانات
# ======================================================
DB_NAME = "shop.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        balance REAL DEFAULT 0,
        referral_points INTEGER DEFAULT 0,
        is_banned INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        product_name TEXT,
        price REAL,
        quantity INTEGER DEFAULT 1,
        status TEXT DEFAULT 'pending',
        details TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

init_db()

# ======================================================
# 3. دوال مساعدة
# ======================================================
def is_admin(user_id):
    return user_id == ADMIN_ID

def get_balance(user_id):
    conn = get_db()
    r = conn.cursor().execute('SELECT balance FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return r[0] if r else 0.0

def create_order(user_id, product_name, price, qty=1, details=""):
    conn = get_db()
    c = conn.cursor()
    c.execute('''INSERT INTO orders (user_id, product_name, price, quantity, details, status)
                 VALUES (?, ?, ?, ?, ?, 'pending')''', (user_id, product_name, price, qty, details))
    conn.commit()
    oid = c.lastrowid
    conn.close()
    return oid

def add_purchase_points(user_id):
    conn = get_db()
    conn.cursor().execute('UPDATE users SET referral_points = referral_points + 1 WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()

# ======================================================
# 4. القوائم
# ======================================================
MAIN_MENU = [
    [InlineKeyboardButton("🎮 الحسابات", callback_data="cat_acc")],
    [InlineKeyboardButton("👥 المتابعين", callback_data="cat_fol")],
    [InlineKeyboardButton("📞 الأرقام", callback_data="cat_num")],
    [InlineKeyboardButton("⭐ النجوم", callback_data="cat_star")],
    [InlineKeyboardButton("👤 اليوزرات", callback_data="cat_user")],
    [InlineKeyboardButton("🔗 إحالات البوتات", callback_data="cat_ref")],
    [InlineKeyboardButton("💳 شحن الرصيد", callback_data="cat_recharge")],
    [InlineKeyboardButton("📢 تمويل القنوات", callback_data="cat_fund")],
    [InlineKeyboardButton("🛒 سلة المشتريات", callback_data="view_cart")],
    [InlineKeyboardButton("📞 تواصل معنا", callback_data="contact")],
]

ADMIN_MENU = [
    [InlineKeyboardButton("📊 الإحصائيات", callback_data="admin_stats")],
    [InlineKeyboardButton("🚫 حظر مستخدم", callback_data="admin_ban")],
    [InlineKeyboardButton("📢 إذاعة", callback_data="admin_broadcast")],
    [InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")],
]

# ======================================================
# 5. أوامر البوت
# ======================================================
async def start(update: Update, context):
    user = update.effective_user
    uid = user.id
    uname = user.username or "لا يوجد"
    fname = user.first_name or "صديقنا"

    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO users (id, username, first_name, balance, referral_points) VALUES (?, ?, ?, 0, 0)',
              (uid, uname, fname))
    conn.commit()
    r = c.execute('SELECT referral_points, balance FROM users WHERE id = ?', (uid,)).fetchone()
    conn.close()
    points = r[0] if r else 0
    balance = r[1] if r else 0

    text = f"""👋 مرحباً بك يا {fname}
👾 أهلاً وسهلاً بك في {SHOP_NAME} 👾
━━━━━━━━━━
📌 معلوماتك :
✅ ايدي حسابك : `{uid}`
👤 يوزرك : @{uname}
⭐️ نقاطك : {points}
💰 رصيدك : {balance}$
━━━━━━━━━━
🤔 نتمنى لك تجربة ممتعة 🤔"""

    keyboard = MAIN_MENU.copy()
    if is_admin(uid):
        keyboard.append([InlineKeyboardButton("⚙️ لوحة الأدمن", callback_data="admin_panel")])
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()
    data = query.data
    uid = query.from_user.id

    if data == "back_to_main":
        keyboard = MAIN_MENU.copy()
        if is_admin(uid):
            keyboard.append([InlineKeyboardButton("⚙️ لوحة الأدمن", callback_data="admin_panel")])
        await query.edit_message_text(f"📋 **القائمة الرئيسية - {SHOP_NAME}**",
                                      reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')
        return

    if data == "contact":
        await query.edit_message_text(f"📞 **تواصل معنا**\n\nللدعم: {SUPPORT_USERNAME}\n[اضغط هنا]({SUPPORT_LINK})",
                                      parse_mode='Markdown', disable_web_page_preview=True)
        return

    if data == "view_cart":
        conn = get_db()
        orders = conn.cursor().execute('''SELECT id, product_name, price, status, created_at
                                          FROM orders WHERE user_id = ?
                                          ORDER BY created_at DESC LIMIT 50''', (uid,)).fetchall()
        conn.close()
        if not orders:
            await query.edit_message_text("🛒 **سلة المشتريات**\n\n📭 ليس لديك أي طلبات سابقة.", parse_mode='Markdown')
            return
        msg = "🛒 **طلباتي**\n━━━━━━━━━━━━━━━━\n"
        for o in orders:
            emoji = {'pending': '⏳', 'completed': '✅', 'cancelled': '❌'}.get(o['status'], '📦')
            msg += f"{emoji} #{o['id']} - {o['product_name']} - {o['price']}$\n"
        await query.edit_message_text(msg, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 رجوع", callback_data="back_to_main")]]), parse_mode='Markdown')
        return

    if data.startswith("cat_"):
        await query.edit_message_text(f"⏳ **قيد التطوير**\n\nهذا القسم سيتم إضافته قريباً.", parse_mode='Markdown')
        return

    if data == "admin_panel":
        await admin_panel(update, context)
        return
    if data == "admin_stats":
        await admin_stats(update, context)
        return
    if data == "admin_ban":
        await ban_user_start(update, context)
        return
    if data == "admin_broadcast":
        await broadcast_start(update, context)
        return

    await query.edit_message_text("❌ خيار غير معروف", parse_mode='Markdown')

# ======================================================
# 6. لوحة الأدمن
# ======================================================
async def admin_panel(update, context):
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id):
        await q.edit_message_text("⛔ هذا القسم للمدير فقط!")
        return
    await q.edit_message_text("⚙️ **لوحة تحكم الأدمن**", reply_markup=InlineKeyboardMarkup(ADMIN_MENU), parse_mode='Markdown')

async def admin_stats(update, context):
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id):
        await q.edit_message_text("⛔ للمدير فقط!")
        return
    conn = get_db()
    c = conn.cursor()
    users = c.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    orders = c.execute('SELECT COUNT(*) FROM orders').fetchone()[0]
    pending = c.execute('SELECT COUNT(*) FROM orders WHERE status="pending"').fetchone()[0]
    earnings = c.execute('SELECT SUM(price) FROM orders WHERE status="completed"').fetchone()[0] or 0
    conn.close()
    await q.edit_message_text(f"📊 **الإحصائيات**\n👤 المستخدمين: {users}\n📦 الطلبات: {orders}\n🔄 المعلقة: {pending}\n💰 الأرباح: {earnings:.2f}$", parse_mode='Markdown')

# ======================================================
# 7. حظر وإذاعة
# ======================================================
async def ban_user_start(update, context):
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id):
        await q.edit_message_text("⛔ للمدير فقط!")
        return
    await q.edit_message_text("🚫 أرسل ID المستخدم للحظر:", parse_mode='Markdown')
    return 'WAITING_BAN'

async def ban_user_confirm(update, context):
    try:
        uid = int(update.message.text.strip())
        conn = get_db()
        conn.cursor().execute('UPDATE users SET is_banned = 1 WHERE id = ?', (uid,))
        conn.commit()
        conn.close()
        await update.message.reply_text(f"✅ تم حظر المستخدم `{uid}`", parse_mode='Markdown')
    except:
        await update.message.reply_text("❌ ID غير صحيح، أرسل أرقام فقط.")
    return ConversationHandler.END

async def broadcast_start(update, context):
    q = update.callback_query
    await q.answer()
    if not is_admin(q.from_user.id):
        await q.edit_message_text("⛔ للمدير فقط!")
        return
    await q.edit_message_text("📢 أرسل رسالة الإذاعة (يدعم Markdown):", parse_mode='Markdown')
    return 'WAITING_BROADCAST'

async def broadcast_send(update, context):
    msg = update.message.text
    conn = get_db()
    users = conn.cursor().execute('SELECT id FROM users WHERE is_banned = 0').fetchall()
    conn.close()
    success, fail = 0, 0
    for u in users:
        try:
            await context.bot.send_message(chat_id=u['id'], text=msg, parse_mode='Markdown')
            success += 1
        except:
            fail += 1
    await update.message.reply_text(f"✅ تم الإرسال لـ {success} مستخدم.\n❌ فشل الإرسال لـ {fail} مستخدم.", parse_mode='Markdown')
    return ConversationHandler.END

async def cancel(update, context):
    await update.message.reply_text("❌ تم إلغاء العملية.", parse_mode='Markdown')
    return ConversationHandler.END

# ======================================================
# 8. التشغيل
# ======================================================
def main():
    logging.basicConfig(level=logging.INFO)
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    ban_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(ban_user_start, pattern="^admin_ban$")],
        states={'WAITING_BAN': [MessageHandler(filters.TEXT & ~filters.COMMAND, ban_user_confirm)]},
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    broadcast_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(broadcast_start, pattern="^admin_broadcast$")],
        states={'WAITING_BROADCAST': [MessageHandler(filters.TEXT & ~filters.COMMAND, broadcast_send)]},
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(ban_conv)
    app.add_handler(broadcast_conv)

    print("✅ البوت شغال...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
