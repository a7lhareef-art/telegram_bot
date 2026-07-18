import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
import json
import os
import random
import time
import re

# ====== توكن البوت ======
BOT_TOKEN = "8919242004:AAFPIbZDSLTT0OZblIyKby_IlD96UeQGD8k"

bot = telebot.TeleBot(BOT_TOKEN)

# ====== معرف المشرف ======
ADMIN_ID = 123456789  # 👈 غير ده بمعرفك

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

# ====== باقات البروكسي ======
PROXY_PACKAGES = {
    "2 hours": 25,
    "6 hours": 35,
    "12 hours": 50,
    "1 day": 90,
    "2 days": 170,
    "7 days": 500,
    "10 days": 750,
    "14 days": 1000,
    "30 days": 1700
}

# ====== سيرفرات البروكسي ======
PROXY_SERVERS = {
    "🇺🇸 أمريكا": {
        "code": "USA",
        "servers": [
            "Florida2 - T-Mobile - 15min",
            "California - Verizon - 30min",
            "Florida - T-Mobile - 30min",
            "NewYork - T-Mobile - 30min",
            "NewYork3 - Verizon - 30min",
            "NewYork - Verizon - 30min",
            "NewYork2 - Verizon - 30min",
            "Newjersey - AT&T - 30min",
            "Newjersey2 - T-Mobile - 30min",
            "Brooklyn - T-mobile - 60min",
            "Delaware - Verizon - 30min",
            "Pittsburgh - Verizon - 30min",
            "Texas - T-Mobile - 30min"
        ]
    },
    "🇬🇧 بريطانيا": {
        "code": "UK",
        "servers": ["London - Three - 30min"]
    },
    "🇩🇪 ألمانيا": {
        "code": "DE",
        "servers": ["Hanover - 02 - 30min"]
    },
    "🇫🇷 فرنسا": {
        "code": "FR",
        "servers": ["Nice - SFR - 30min"]
    },
    "🇮🇹 إيطاليا": {
        "code": "IT",
        "servers": ["Bussolengo - Wind Tre - 30min"]
    }
}

# ====== أرقام تليجرام تجريبية ======
TELEGRAM_NUMBERS = {
    "🇪🇬 مصر": "+201012345678",
    "🇺🇸 أمريكا": "+19876543210",
    "🇬🇧 بريطانيا": "+447912345678",
    "🇨🇦 كندا": "+16471234567",
    "🇦🇺 أستراليا": "+61491234567",
    "🇩🇪 ألمانيا": "+4915123456789",
    "🇫🇷 فرنسا": "+33612345678",
    "🇮🇹 إيطاليا": "+39123456789",
    "🇹🇷 تركيا": "+905551234567"
}

WHATSAPP_NUMBERS = {
    "🇪🇬 واتساب مصر": "+201098765432",
    "🇺🇸 واتساب أمريكا": "+18765432109",
    "🇬🇧 واتساب بريطانيا": "+447923456789",
    "🇨🇦 واتساب كندا": "+16472345678",
    "🇦🇺 واتساب أستراليا": "+61492345678",
    "🇩🇪 واتساب ألمانيا": "+4915234567890"
}

# ====== الأزرار الرئيسية ======
main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add(
    KeyboardButton("🌐 احصل على بروكسي"),
    KeyboardButton("🎯 خدمات الرشق"),
    KeyboardButton("📱 أرقام تليجرام")
)
main_keyboard.add(
    KeyboardButton("💬 أرقام واتساب"),
    KeyboardButton("💰 شحن رصيد"),
    KeyboardButton("📋 حالة طلبي")
)
main_keyboard.add(
    KeyboardButton("📊 إحصائياتي"),
    KeyboardButton("ℹ️ عن البوت")
)

# ====== أزرار البروكسي ======
proxy_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
for country in PROXY_SERVERS.keys():
    proxy_keyboard.add(KeyboardButton(country))
proxy_keyboard.add(KeyboardButton("🔙 رجوع"))

# ====== أزرار سيرفرات البروكسي ======
server_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

# ====== أزرار المدة ======
duration_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
duration_keyboard.add(
    KeyboardButton("2 hours"),
    KeyboardButton("6 hours"),
    KeyboardButton("12 hours")
)
duration_keyboard.add(
    KeyboardButton("1 day"),
    KeyboardButton("2 days"),
    KeyboardButton("7 days")
)
duration_keyboard.add(
    KeyboardButton("10 days"),
    KeyboardButton("14 days"),
    KeyboardButton("30 days")
)
duration_keyboard.add(KeyboardButton("🔙 رجوع"))

# ====== أزرار البروتوكول ======
protocol_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
protocol_keyboard.add(
    KeyboardButton("🔗 HTTP"),
    KeyboardButton("🔒 SOCKS5")
)
protocol_keyboard.add(KeyboardButton("🔙 رجوع"))

# ====== أزرار الرشق ======
rashq_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
rashq_keyboard.add(
    KeyboardButton("📱 رشق تليجرام"),
    KeyboardButton("💬 رشق واتساب"),
    KeyboardButton("📸 رشق إنستغرام")
)
rashq_keyboard.add(
    KeyboardButton("🐦 رشق تويتر"),
    KeyboardButton("🎯 رشق مخصص"),
    KeyboardButton("🔙 رجوع")
)

# ====== أزرار أرقام تليجرام ======
telegram_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
telegram_keyboard.add(
    KeyboardButton("🇪🇬 مصر"),
    KeyboardButton("🇺🇸 أمريكا"),
    KeyboardButton("🇬🇧 بريطانيا")
)
telegram_keyboard.add(
    KeyboardButton("🇨🇦 كندا"),
    KeyboardButton("🇦🇺 أستراليا"),
    KeyboardButton("🇩🇪 ألمانيا")
)
telegram_keyboard.add(
    KeyboardButton("🇫🇷 فرنسا"),
    KeyboardButton("🇮🇹 إيطاليا"),
    KeyboardButton("🇹🇷 تركيا")
)
telegram_keyboard.add(KeyboardButton("🔙 رجوع"))

# ====== أزرار واتساب ======
whatsapp_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
whatsapp_keyboard.add(
    KeyboardButton("🇪🇬 واتساب مصر"),
    KeyboardButton("🇺🇸 واتساب أمريكا"),
    KeyboardButton("🇬🇧 واتساب بريطانيا")
)
whatsapp_keyboard.add(
    KeyboardButton("🇨🇦 واتساب كندا"),
    KeyboardButton("🇦🇺 واتساب أستراليا"),
    KeyboardButton("🇩🇪 واتساب ألمانيا")
)
whatsapp_keyboard.add(KeyboardButton("🔙 رجوع"))

# ====== أزرار شحن الرصيد ======
payment_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
payment_keyboard.add(
    KeyboardButton("🏦 تحويل بنكي"),
    KeyboardButton("📱 فودافون كاش"),
    KeyboardButton("💳 إنستا باي")
)
payment_keyboard.add(
    KeyboardButton("💵 باي بال"),
    KeyboardButton("🪙 USDT"),
    KeyboardButton("🔙 رجوع")
)

# ====== متغيرات مؤقتة ======
user_temp_data = {}

# ============================================
# ====== دوال البيانات ======
# ============================================

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

# ============================================
# ====== دوال المستخدمين ======
# ============================================

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
        "balance": 0,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_data(data)
    try:
        bot.send_message(ADMIN_ID, f"🆕 مستخدم جديد!\n👤 {first_name}\n🆔 `{user_id}`", parse_mode='Markdown')
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

# ============================================
# ====== التحقق من الاشتراك ======
# ============================================

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

# ============================================
# ====== دوال التفعيل ======
# ============================================

def send_activation_message(user_id, username, first_name, service_type, data, order_id, is_trial=True):
    try:
        msg = (
            f"🔔 **عملية تفعيل جديدة**\n\n"
            f"┏━━━━━━━━━━━━━━━━━━━━━┓\n"
            f"┃ 📋 رقم الطلب: `{order_id}`\n"
            f"┃ 👤 المستخدم: {first_name}\n"
            f"┃ 🆔 المعرف: `{user_id}`\n"
            f"┃ 📛 اليوزر: @{username if username else 'لا يوجد'}\n"
            f"┃ 🎯 الخدمة: {service_type}\n"
        )
        
        if service_type == "بروكسي":
            msg += (
                f"┃ 🌍 الدولة: {data.get('country', '')}\n"
                f"┃ 🖥️ السيرفر: {data.get('server', '')}\n"
                f"┃ ⏱ المدة: {data.get('duration', '')}\n"
                f"┃ 🔒 البروتوكول: {data.get('protocol', '')}\n"
                f"┃ 🌐 IP: {data.get('ip', '')}\n"
                f"┃ 🔢 Port: {data.get('port', '')}\n"
                f"┃ 👤 Username: {data.get('username', '')}\n"
                f"┃ 🔑 Password: {data.get('password', '')}\n"
                f"┃ 📅 الانتهاء: {data.get('expiry', '')}\n"
            )
        else:
            msg += (
                f"┃ 🌍 الدولة: {data.get('country', '')}\n"
                f"┃ 📱 الرقم: `{data.get('number', '')}`\n"
            )
        
        msg += f"┗━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        msg += f"🎁 **تجريبي**" if is_trial else "💳 **شراء**"
        
        bot.send_message(ACTIVATION_CHANNEL_ID, msg, parse_mode='Markdown')
    except Exception as e:
        print(f"خطأ في إرسال التفعيل: {e}")

# ============================================
# ====== دوال البروكسي ======
# ============================================

def generate_proxy_data(country, server, protocol, username, password, duration):
    ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    port = random.randint(1000, 9999)
    
    days_map = {
        "2 hours": 0.08, "6 hours": 0.25, "12 hours": 0.5,
        "1 day": 1, "2 days": 2, "7 days": 7,
        "10 days": 10, "14 days": 14, "30 days": 30
    }
    days = days_map.get(duration, 1)
    expiry = datetime.now() + timedelta(days=days)
    
    return {
        "ip": ip,
        "port": port,
        "protocol": protocol,
        "username": username,
        "password": password,
        "expiry": expiry.strftime("%Y-%m-%d %H:%M:%S"),
        "duration": duration,
        "country": country,
        "server": server
    }

def get_server_keyboard(country):
    """إنشاء أزرار السيرفرات لدولة معينة"""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    servers = PROXY_SERVERS.get(country, {}).get("servers", [])
    for server in servers:
        keyboard.add(KeyboardButton(server))
    keyboard.add(KeyboardButton("🔙 رجوع"))
    return keyboard

# ============================================
# ====== أوامر البوت ======
# ============================================

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
    trial_count = user_data.get("trial_count", 0) if user_data else 0
    remaining = 3 - trial_count
    balance = user_data.get("balance", 0) if user_data else 0
    
    bot.send_message(
        message.chat.id,
        f"👋 أهلاً بك {first_name}!\n\n"
        "🏢 **متجر الخدمات الشامل**\n\n"
        f"🎁 التجارب المتبقية: {remaining}\n"
        f"💰 الرصيد: {balance} نقطة\n\n"
        "📌 اختر الخدمة المناسبة 👇",
        reply_markup=main_keyboard
    )

@bot.message_handler(commands=['proxy'])
def proxy_command(message):
    if not is_user_subscribed(message.from_user.id):
        start_command(message)
        return
    bot.send_message(
        message.chat.id,
        "🌐 **اختر الدولة المطلوبة:**\n\n"
        "🇺🇸 أمريكا - 13 سيرفر\n"
        "🇬🇧 بريطانيا - 1 سيرفر\n"
        "🇩🇪 ألمانيا - 1 سيرفر\n"
        "🇫🇷 فرنسا - 1 سيرفر\n"
        "🇮🇹 إيطاليا - 1 سيرفر",
        reply_markup=proxy_keyboard
    )

@bot.message_handler(commands=['rashq'])
def rashq_command(message):
    if not is_user_subscribed(message.from_user.id):
        start_command(message)
        return
    bot.send_message(
        message.chat.id,
        "🎯 **خدمات الرشق**\n\n"
        "اختر الخدمة المطلوبة 👇\n\n"
        "📱 رشق تليجرام - 3$ (1000 متابع)\n"
        "💬 رشق واتساب - 4$ (500 متابع)\n"
        "📸 رشق إنستغرام - 5$ (500 متابع)\n"
        "🐦 رشق تويتر - 4.5$ (500 متابع)",
        reply_markup=rashq_keyboard
    )

@bot.message_handler(commands=['telegram'])
def telegram_command(message):
    if not is_user_subscribed(message.from_user.id):
        start_command(message)
        return
    bot.send_message(
        message.chat.id,
        "📱 **أرقام تليجرام**\n\n"
        "اختر الدولة 👇\n\n"
        "⚡ أرقام نشطة وجاهزة للاستخدام",
        reply_markup=telegram_keyboard
    )

@bot.message_handler(commands=['whatsapp'])
def whatsapp_command(message):
    if not is_user_subscribed(message.from_user.id):
        start_command(message)
        return
    bot.send_message(
        message.chat.id,
        "💬 **أرقام واتساب**\n\n"
        "اختر الدولة 👇\n\n"
        "⚡ أرقام مفعلة وجاهزة للاستخدام",
        reply_markup=whatsapp_keyboard
    )

@bot.message_handler(commands=['payment'])
def payment_command(message):
    if not is_user_subscribed(message.from_user.id):
        start_command(message)
        return
    bot.send_message(
        message.chat.id,
        "💰 **شحن الرصيد**\n\n"
        "اختر طريقة الدفع 👇\n\n"
        "📌 الحد الأدنى للشحن: 10$",
        reply_markup=payment_keyboard
    )

@bot.message_handler(commands=['balance'])
def balance_command(message):
    if not is_user_subscribed(message.from_user.id):
        start_command(message)
        return
    user_data = get_user_data(message.from_user.id)
    balance = user_data.get("balance", 0) if user_data else 0
    trial_count = user_data.get("trial_count", 0) if user_data else 0
    
    bot.send_message(
        message.chat.id,
        f"📊 **إحصائياتك:**\n\n"
        f"💰 الرصيد: {balance} نقطة\n"
        f"🎁 التجارب المستخدمة: {trial_count}/3\n"
        f"📅 تاريخ التسجيل: {user_data.get('date', 'غير معروف') if user_data else 'غير معروف'}"
    )

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
    
    msg = "📋 **طلباتك:**\n\n"
    for order in user_orders[-5:]:
        msg += f"┃ {order['order_id']}\n"
        msg += f"┃ 🎯 {order.get('service_type', '')}\n"
        msg += f"┃ 🌍 {order.get('country', '')}\n"
        msg += f"┃ 📌 الحالة: {order.get('status', '')}\n"
        msg += f"┗━━━━━━━━━━━━━━━━━┛\n\n"
    
    bot.send_message(message.chat.id, msg, reply_markup=main_keyboard)

@bot.message_handler(commands=['about'])
def about_command(message):
    bot.send_message(
        message.chat.id,
        "🤖 **عن البوت:**\n\n"
        "🏢 متجر الخدمات الشامل\n"
        "📦 الإصدار: 7.0\n"
        "🔄 يعمل 24/7\n\n"
        "✨ **الخدمات:**\n"
        "• 🌐 بروكسي - 5 دول - 17 سيرفر\n"
        "• 🎯 خدمات الرشق\n"
        "• 📱 أرقام تليجرام\n"
        "• 💬 أرقام واتساب\n\n"
        "🎁 **3 تجارب مجانية**\n"
        "💰 نظام نقاط للشحن",
        reply_markup=main_keyboard
    )

# ============================================
# ====== معالج الاشتراك ======
# ============================================

@bot.callback_query_handler(func=lambda call: call.data == "check_subscribe")
def check_subscribe_callback(call):
    user_id = call.from_user.id
    is_subscribed, channel = check_subscription(user_id)
    
    if is_subscribed:
        bot.edit_message_text(
            "✅ **تم التحقق من اشتراكك!**\n\n"
            "🎉 يمكنك الآن استخدام البوت.",
            call.message.chat.id,
            call.message.message_id
        )
        start_command(call.message)
    else:
        bot.answer_callback_query(
            call.id,
            f"❌ لم تشترك في قناة {channel} بعد!",
            show_alert=True
        )

# ============================================
# ====== الأزرار العادية ======
# ============================================

@bot.message_handler(func=lambda message: message.text == "🌐 احصل على بروكسي")
def proxy_button(message):
    proxy_command(message)

@bot.message_handler(func=lambda message: message.text == "🎯 خدمات الرشق")
def rashq_button(message):
    rashq_command(message)

@bot.message_handler(func=lambda message: message.text == "📱 أرقام تليجرام")
def telegram_button(message):
    telegram_command(message)

@bot.message_handler(func=lambda message: message.text == "💬 أرقام واتساب")
def whatsapp_button(message):
    whatsapp_command(message)

@bot.message_handler(func=lambda message: message.text == "💰 شحن رصيد")
def payment_button(message):
    payment_command(message)

@bot.message_handler(func=lambda message: message.text == "📋 حالة طلبي")
def status_button(message):
    status_command(message)

@bot.message_handler(func=lambda message: message.text == "📊 إحصائياتي")
def balance_button(message):
    balance_command(message)

@bot.message_handler(func=lambda message: message.text == "ℹ️ عن البوت")
def about_button(message):
    about_command(message)

# ============================================
# ====== اختيار دولة البروكسي ======
# ============================================

@bot.message_handler(func=lambda message: message.text in PROXY_SERVERS.keys())
def select_proxy_country(message):
    user_id = message.from_user.id
    country = message.text
    
    # حفظ الدولة في البيانات المؤقتة
    if user_id not in user_temp_data:
        user_temp_data[user_id] = {}
    user_temp_data[user_id]["country"] = country
    
    # عرض السيرفرات
    bot.send_message(
        message.chat.id,
        f"🌐 **{country}**\n\n"
        "اختر السيرفر المطلوب 👇",
        reply_markup=get_server_keyboard(country)
    )

# ============================================
# ====== اختيار سيرفر البروكسي ======
# ============================================

@bot.message_handler(func=lambda message: any(message.text in servers for servers in [s["servers"] for s in PROXY_SERVERS.values()]))
def select_proxy_server(message):
    user_id = message.from_user.id
    server = message.text
    
    # حفظ السيرفر في البيانات المؤقتة
    if user_id not in user_temp_data:
        user_temp_data[user_id] = {}
    user_temp_data[user_id]["server"] = server
    
    # عرض المدة
    bot.send_message(
        message.chat.id,
        f"🖥️ **السيرفر: {server}**\n\n"
        "⏱ اختر المدة المطلوبة:\n\n"
        "2 hours - 25 نقطة\n"
        "6 hours - 35 نقطة\n"
        "12 hours - 50 نقطة\n"
        "1 day - 90 نقطة\n"
        "2 days - 170 نقطة\n"
        "7 days - 500 نقطة\n"
        "10 days - 750 نقطة\n"
        "14 days - 1000 نقطة\n"
        "30 days - 1700 نقطة",
        reply_markup=duration_keyboard
    )

# ============================================
# ====== اختيار مدة البروكسي ======
# ============================================

@bot.message_handler(func=lambda message: message.text in PROXY_PACKAGES.keys())
def select_proxy_duration(message):
    user_id = message.from_user.id
    duration = message.text
    
    # حفظ المدة في البيانات المؤقتة
    if user_id not in user_temp_data:
        user_temp_data[user_id] = {}
    user_temp_data[user_id]["duration"] = duration
    
    # عرض البروتوكول
    bot.send_message(
        message.chat.id,
        f"⏱ **المدة: {duration}**\n"
        f"💰 السعر: {PROXY_PACKAGES[duration]} نقطة\n\n"
        "🔒 اختر البروتوكول المطلوب:",
        reply_markup=protocol_keyboard
    )

# ============================================
# ====== اختيار بروتوكول البروكسي ======
# ============================================

@bot.message_handler(func=lambda message: message.text in ["🔗 HTTP", "🔒 SOCKS5"])
def select_proxy_protocol(message):
    user_id = message.from_user.id
    protocol = message.text.replace("🔗 ", "").replace("🔒 ", "")
    
    # حفظ البروتوكول في البيانات المؤقتة
    if user_id not in user_temp_data:
        user_temp_data[user_id] = {}
    user_temp_data[user_id]["protocol"] = protocol
    
    # طلب اسم المستخدم
    bot.send_message(
        message.chat.id,
        f"🔒 **البروتوكول: {protocol}**\n\n"
        "👤 **أرسل اسم المستخدم المطلوب:**"
    )

# ============================================
# ====== استقبال اسم المستخدم ======
# ============================================

@bot.message_handler(func=lambda message: re.match(r'^[a-zA-Z0-9_]{3,20}$', message.text) and message.text not in ["🔙 رجوع", "🌐 احصل على بروكسي", "🎯 خدمات الرشق", "📱 أرقام تليجرام", "💬 أرقام واتساب", "💰 شحن رصيد", "📋 حالة طلبي", "📊 إحصائياتي", "ℹ️ عن البوت"])
def get_proxy_username(message):
    user_id = message.from_user.id
    username_input = message.text
    
    # التحقق من وجود بيانات مؤقتة
    if user_id not in user_temp_data or "country" not in user_temp_data[user_id]:
        bot.send_message(message.chat.id, "⚠️ حدث خطأ، ابدأ من جديد /proxy")
        return
    
    # حفظ اسم المستخدم
    user_temp_data[user_id]["username"] = username_input
    
    # طلب كلمة المرور
    bot.send_message(
        message.chat.id,
        f"👤 **اسم المستخدم: {username_input}**\n\n"
        "🔑 **أرسل كلمة المرور المطلوبة:**"
    )

# ============================================
# ====== استقبال كلمة المرور ======
# ============================================

@bot.message_handler(func=lambda message: len(message.text) >= 4 and message.text not in ["🔙 رجوع", "🌐 احصل على بروكسي", "🎯 خدمات الرشق", "📱 أرقام تليجرام", "💬 أرقام واتساب", "💰 شحن رصيد", "📋 حالة طلبي", "📊 إحصائياتي", "ℹ️ عن البوت"])
def get_proxy_password(message):
    user_id = message.from_user.id
    password_input = message.text
    
    # التحقق من وجود بيانات مؤقتة
    if user_id not in user_temp_data or "username" not in user_temp_data[user_id]:
        bot.send_message(message.chat.id, "⚠️ حدث خطأ، ابدأ من جديد /proxy")
        return
    
    # حفظ كلمة المرور
    user_temp_data[user_id]["password"] = password_input
    
    # عرض ملخص الطلب
    data = user_temp_data[user_id]
    
    # التحقق من التجربة
    is_trial = can_use_trial(user_id)
    price = PROXY_PACKAGES.get(data.get("duration", "1 day"), 90)
    
    if not is_trial:
        # التحقق من الرصيد
        user_data = get_user_data(user_id)
        balance = user_data.get("balance", 0) if user_data else 0
        if balance < price:
            bot.send_message(
                message.chat.id,
                f"❌ **رصيد غير كافٍ!**\n\n"
                f"💰 رصيدك: {balance} نقطة\n"
                f"💳 المطلوب: {price} نقطة\n\n"
                "📌 اضغط: 💰 شحن رصيد",
                reply_markup=main_keyboard
            )
            return
    
    # توليد البروكسي
    proxy_data = generate_proxy_data(
        data.get("country", ""),
        data.get("server", ""),
        data.get("protocol", "SOCKS5"),
        data.get("username", ""),
        data.get("password", ""),
        data.get("duration", "1 day")
    )
    
    # إنشاء الطلب
    order_id = generate_order_id()
    orders = load_orders()
    orders.append({
        "order_id": order_id,
        "user_id": user_id,
        "service_type": "بروكسي",
        "country": data.get("country", ""),
        "server": data.get("server", ""),
        "duration": data.get("duration", ""),
        "protocol": data.get("protocol", ""),
        "ip": proxy_data["ip"],
        "port": proxy_data["port"],
        "username": data.get("username", ""),
        "password": data.get("password", ""),
        "expiry": proxy_data["expiry"],
        "price": price if not is_trial else 0,
        "is_trial": is_trial,
        "status": "✅ تم التسليم",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_orders(orders)
    
    # زيادة عدد التجارب
    if is_trial:
        increment_trial(user_id)
    
    # إرسال البروكسي للمستخدم
    bot.send_message(
        message.chat.id,
        f"✅ **تم شراء البروكسي بنجاح!**\n\n"
        f"┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
        f"┃ 📋 رقم الطلب: `{order_id}`\n"
        f"┃ 🌍 الدولة: {data.get('country', '')}\n"
        f"┃ 🖥️ السيرفر: {data.get('server', '')}\n"
        f"┃ ⏱ المدة: {data.get('duration', '')}\n"
        f"┃ 🔒 البروتوكول: {data.get('protocol', '')}\n"
        f"┃ 🌐 IP: `{proxy_data['ip']}`\n"
        f"┃ 🔢 Port: `{proxy_data['port']}`\n"
        f"┃ 👤 Username: `{data.get('username', '')}`\n"
        f"┃ 🔑 Password: `{data.get('password', '')}`\n"
        f"┃ 📅 الانتهاء: {proxy_data['expiry']}\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        f"{'🎁 **تجربة مجانية**' if is_trial else f'💳 **تم الخصم: {price} نقطة**'}\n\n"
        "📌 يمكنك استخدام البروكسي فوراً ✅",
        parse_mode='Markdown',
        reply_markup=main_keyboard
    )
    
    # إرسال نسخة لقناة التفعيلات
    send_activation_message(
        user_id,
        message.from_user.username or "لا يوجد",
        message.from_user.first_name,
        "بروكسي",
        {
            "country": data.get("country", ""),
            "server": data.get("server", ""),
            "duration": data.get("duration", ""),
            "protocol": data.get("protocol", ""),
            "ip": proxy_data["ip"],
            "port": proxy_data["port"],
            "username": data.get("username", ""),
            "password": data.get("password", ""),
            "expiry": proxy_data["expiry"],
            "is_trial": is_trial
        },
        order_id,
        is_trial
    )
    
    # حذف البيانات المؤقتة
    if user_id in user_temp_data:
        del user_temp_data[user_id]

# ============================================
# ====== زر الرجوع ======
# ============================================

@bot.message_handler(func=lambda message: message.text == "🔙 رجوع")
def back_button(message):
    start_command(message)

# ============================================
# ====== تشغيل البوت ======
# ============================================

if __name__ == "__main__":
    print("🚀 البوت شغال...")
    print("🌐 5 دول - 17 سيرفر بروكسي")
    print("🎁 3 تجارب مجانية لكل مستخدم")
    print("📅", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 40)
    
    bot.infinity_polling()
