import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import json
import os
import time
import random

# ====== توكن البوت ======
BOT_TOKEN = "8919242004:AAFPIbZDSLTT0OZblIyKby_IlD96UeQGD8k"

bot = telebot.TeleBot(BOT_TOKEN)

# ====== معرف المشرف ======
ADMIN_ID = 123456789  # 👈 غير ده بمعرفك الشخصي

# ====== قنوات الاشتراك الإجباري ======
REQUIRED_CHANNELS = [
    {"username": "PrimeStore065", "link": "https://t.me/PrimeStore065"},
    {"username": "primestoreActivations", "link": "https://t.me/primestoreActivations"},
    {"username": "freeproiftking", "link": "https://t.me/freeproiftking"},
]

ACTIVATION_CHANNEL_ID = "@primestoreActivations"

# ====== ملفات البيانات ======
DATA_FILE = "data.json"
ORDERS_FILE = "orders.json"

# ====== أرقام تجريبية ======
TRIAL_NUMBERS = {
    "🇪🇬 مصر": ["+201012345678", "+201098765432", "+201055512345"],
    "🇺🇸 أمريكا": ["+19876543210", "+18765432109", "+17654321098"],
    "🇬🇧 بريطانيا": ["+447912345678", "+447923456789", "+447934567890"],
    "🇨🇦 كندا": ["+16471234567", "+16472345678", "+16473456789"],
    "🇦🇺 أستراليا": ["+61491234567", "+61492345678", "+61493456789"],
    "🇩🇪 ألمانيا": ["+4915123456789", "+4915234567890", "+4915345678901"],
    "🇫🇷 فرنسا": ["+33612345678", "+33623456789", "+33634567890"],
    "🇮🇹 إيطاليا": ["+39123456789", "+39234567890", "+39345678901"],
    "🇪🇸 إسبانيا": ["+34612345678", "+34623456789", "+34634567890"],
    "🇹🇷 تركيا": ["+905551234567", "+905552345678", "+905553456789"]
}

PRICES = {"🇪🇬 مصر": 0.30, "🌍 باقي الدول": "0.15 - 0.70"}

# ====== دوال البيانات ======
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"users": []}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_orders():
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_orders(orders):
    with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

def register_user(user_id, username, first_name):
    data = load_data()
    for user in data["users"]:
        if user["id"] == user_id:
            return False
    data["users"].append({
        "id": user_id,
        "username": username,
        "first_name": first_name,
        "trial_count": 0,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_data(data)
    try:
        bot.send_message(ADMIN_ID, f"🆕 مستخدم جديد!\n👤 {first_name}\n🆔 `{user_id}`")
    except:
        pass
    return True

def get_user_data(user_id):
    data = load_data()
    for user in data["users"]:
        if user["id"] == user_id:
            return user
    return None

def get_users_count():
    data = load_data()
    return len(data["users"])

def can_use_trial(user_id):
    user_data = get_user_data(user_id)
    if not user_data:
        return False
    return user_data.get("trial_count", 0) < 3

def increment_trial(user_id):
    data = load_data()
    for user in data["users"]:
        if user["id"] == user_id:
            user["trial_count"] = user.get("trial_count", 0) + 1
            save_data(data)
            return True
    return False

def generate_order_id():
    return f"ORD-{datetime.now().strftime('%Y%m%d')}-{int(time.time()) % 10000}"

def get_trial_number(country):
    if country in TRIAL_NUMBERS:
        return random.choice(TRIAL_NUMBERS[country])
    return None

# ====== التحقق من الاشتراك ======
def check_subscription(user_id):
    try:
        for channel in REQUIRED_CHANNELS:
            chat_member = bot.get_chat_member(f"@{channel['username']}", user_id)
            if chat_member.status in ["left", "kicked"]:
                return False, channel['username']
        return True, None
    except:
        return False, REQUIRED_CHANNELS[0]['username']

def get_subscription_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    for channel in REQUIRED_CHANNELS:
        keyboard.add(InlineKeyboardButton(f"📢 اشترك في {channel['username']}", url=channel['link']))
    keyboard.add(InlineKeyboardButton("✅ تم الاشتراك", callback_data="check_subscribe"))
    return keyboard

def is_user_subscribed(user_id):
    is_sub, _ = check_subscription(user_id)
    return is_sub

def send_activation_message(user_id, username, first_name, country, number, order_id):
    try:
        msg = f"🔔 **عملية تفعيل جديدة**\n\n┃ 📋 {order_id}\n┃ 👤 {first_name}\n┃ 🆔 `{user_id}`\n┃ 🌍 {country}\n┃ 📱 `{number}`\n┃ 🎁 تجريبي"
        bot.send_message(ACTIVATION_CHANNEL_ID, msg, parse_mode='Markdown')
    except:
        pass

# ====== الأزرار ======
main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add(KeyboardButton("💰 الأسعار"), KeyboardButton("📞 شراء رقم (تجربة)"), KeyboardButton("🎁 عدد التجارب"))
main_keyboard.add(KeyboardButton("💳 طرق الدفع"), KeyboardButton("📋 حالة طلبي"), KeyboardButton("ℹ️ عن البوت"))

buy_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
buy_keyboard.add(KeyboardButton("🇪🇬 مصر"), KeyboardButton("🌍 باقي الدول"))
buy_keyboard.add(KeyboardButton("🔙 رجوع"))

countries_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
countries_keyboard.add(KeyboardButton("🇺🇸 أمريكا"), KeyboardButton("🇬🇧 بريطانيا"), KeyboardButton("🇨🇦 كندا"))
countries_keyboard.add(KeyboardButton("🇦🇺 أستراليا"), KeyboardButton("🇩🇪 ألمانيا"), KeyboardButton("🇫🇷 فرنسا"))
countries_keyboard.add(KeyboardButton("🇮🇹 إيطاليا"), KeyboardButton("🇪🇸 إسبانيا"), KeyboardButton("🇹🇷 تركيا"))
countries_keyboard.add(KeyboardButton("🔙 رجوع"))

payment_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
payment_keyboard.add(KeyboardButton("🏦 تحويل بنكي"), KeyboardButton("📱 فودافون كاش"), KeyboardButton("💳 إنستا باي"))
payment_keyboard.add(KeyboardButton("🔙 رجوع"))

# ====== أوامر البوت ======
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    username = message.from_user.username or "لا يوجد"
    first_name = message.from_user.first_name
    register_user(user_id, username, first_name)
    
    is_subscribed, _ = check_subscription(user_id)
    if not is_subscribed:
        bot.send_message(message.chat.id, "⚠️ يجب الاشتراك في القنوات!", reply_markup=get_subscription_keyboard())
        return
    
    user_data = get_user_data(user_id)
    remaining = 3 - (user_data.get("trial_count", 0) if user_data else 0)
    bot.send_message(message.chat.id, f"👋 أهلاً {first_name}!\n🎁 التجارب المتبقية: {remaining}", reply_markup=main_keyboard)

@bot.message_handler(commands=['prices'])
def prices_command(message):
    if not is_user_subscribed(message.from_user.id):
        start_command(message)
        return
    bot.send_message(message.chat.id, f"💰 الأسعار:\n🇪🇬 مصر: ${PRICES['🇪🇬 مصر']:.2f}\n🌍 باقي الدول: {PRICES['🌍 باقي الدول']}")

@bot.message_handler(commands=['buy'])
def buy_command(message):
    if not is_user_subscribed(message.from_user.id):
        start_command(message)
        return
    user_id = message.from_user.id
    remaining = 3 - get_user_data(user_id).get("trial_count", 0)
    if remaining <= 0:
        bot.send_message(message.chat.id, "❌ انتهت التجارب!", reply_markup=main_keyboard)
        return
    bot.send_message(message.chat.id, f"📞 اختر الدولة 👇\n🎁 المتبقي: {remaining}", reply_markup=buy_keyboard)

@bot.message_handler(commands=['trial'])
def trial_command(message):
    if not is_user_subscribed(message.from_user.id):
        start_command(message)
        return
    user_data = get_user_data(message.from_user.id)
    trial_count = user_data.get("trial_count", 0) if user_data else 0
    bot.send_message(message.chat.id, f"🎁 عدد التجارب:\n✅ استخدمت: {trial_count}\n🎁 المتبقي: {3 - trial_count}")

@bot.message_handler(commands=['status'])
def status_command(message):
    if not is_user_subscribed(message.from_user.id):
        start_command(message)
        return
    user_id = message.from_user.id
    orders = load_orders()
    user_orders = [o for o in orders if o["user_id"] == user_id]
    if not user_orders:
        bot.send_message(message.chat.id, "📋 لا توجد طلبات", reply_markup=main_keyboard)
        return
    msg = "📋 طلباتك:\n"
    for order in user_orders[-5:]:
        msg += f"┃ {order['order_id']} - {order['country']} - {order.get('number', '')}\n"
    bot.send_message(message.chat.id, msg, reply_markup=main_keyboard)

@bot.message_handler(commands=['payment'])
def payment_command(message):
    if not is_user_subscribed(message.from_user.id):
        start_command(message)
        return
    bot.send_message(message.chat.id, "💳 طرق الدفع", reply_markup=payment_keyboard)

@bot.message_handler(commands=['about'])
def about_command(message):
    bot.send_message(message.chat.id, "🤖 بوت تجريبي\n🎁 3 تجارب مجانية\n🔄 يعمل 24/7", reply_markup=main_keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "check_subscribe")
def check_subscribe_callback(call):
    user_id = call.from_user.id
    is_subscribed, channel = check_subscription(user_id)
    if is_subscribed:
        bot.edit_message_text("✅ تم التحقق!", call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "📌 اختر الخدمة 👇", reply_markup=main_keyboard)
    else:
        bot.answer_callback_query(call.id, f"❌ اشترك في {channel} أولاً!", show_alert=True)

# ====== الأزرار العادية ======
@bot.message_handler(func=lambda message: message.text in ["💰 الأسعار", "📞 شراء رقم (تجربة)", "🎁 عدد التجارب", "📋 حالة طلبي", "💳 طرق الدفع", "ℹ️ عن البوت"])
def handle_buttons(message):
    if message.text == "💰 الأسعار": prices_command(message)
    elif message.text == "📞 شراء رقم (تجربة)": buy_command(message)
    elif message.text == "🎁 عدد التجارب": trial_command(message)
    elif message.text == "📋 حالة طلبي": status_command(message)
    elif message.text == "💳 طرق الدفع": payment_command(message)
    elif message.text == "ℹ️ عن البوت": about_command(message)

@bot.message_handler(func=lambda message: message.text in ["🇪🇬 مصر", "🌍 باقي الدول"])
def select_country_section(message):
    user_id = message.from_user.id
    if not is_user_subscribed(user_id) or not can_use_trial(user_id):
        bot.send_message(message.chat.id, "❌ غير مسموح", reply_markup=main_keyboard)
        return
    
    if message.text == "🇪🇬 مصر":
        country = "🇪🇬 مصر"
        number = get_trial_number(country)
        if number:
            order_id = generate_order_id()
            orders = load_orders()
            orders.append({"order_id": order_id, "user_id": user_id, "country": country, "number": number, "status": "✅ تم", "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            save_orders(orders)
            increment_trial(user_id)
            bot.send_message(message.chat.id, f"✅ الرقم: `{number}`", parse_mode='Markdown')
            send_activation_message(user_id, message.from_user.username or "", message.from_user.first_name, country, number, order_id)
    else:
        bot.send_message(message.chat.id, "🌍 اختر الدولة:", reply_markup=countries_keyboard)

@bot.message_handler(func=lambda message: message.text in ["🇺🇸 أمريكا", "🇬🇧 بريطانيا", "🇨🇦 كندا", "🇦🇺 أستراليا", "🇩🇪 ألمانيا", "🇫🇷 فرنسا", "🇮🇹 إيطاليا", "🇪🇸 إسبانيا", "🇹🇷 تركيا"])
def select_country(message):
    user_id = message.from_user.id
    if not is_user_subscribed(user_id) or not can_use_trial(user_id):
        bot.send_message(message.chat.id, "❌ غير مسموح", reply_markup=main_keyboard)
        return
    
    country = message.text
    number = get_trial_number(country)
    if number:
        order_id = generate_order_id()
        orders = load_orders()
        orders.append({"order_id": order_id, "user_id": user_id, "country": country, "number": number, "status": "✅ تم", "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        save_orders(orders)
        increment_trial(user_id)
        bot.send_message(message.chat.id, f"✅ الرقم: `{number}`", parse_mode='Markdown')
        send_activation_message(user_id, message.from_user.username or "", message.from_user.first_name, country, number, order_id)

@bot.message_handler(func=lambda message: message.text == "🔙 رجوع")
def back_button(message):
    bot.send_message(message.chat.id, "🔙 رجوع", reply_markup=main_keyboard)

@bot.message_handler(func=lambda message: message.text in ["🏦 تحويل بنكي", "📱 فودافون كاش", "💳 إنستا باي"])
def payment_methods(message):
    bot.send_message(message.chat.id, f"📌 {message.text} (للتجربة فقط)", reply_markup=payment_keyboard)

# ====== تشغيل البوت ======
if __name__ == "__main__":
    print("🚀 البوت شغال...")
    bot.infinity_polling()
