import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
import json
import os
import random
import time
import re

# ====== توكن البوت ======
BOT_TOKEN = "8919242004:AAGz2W4nPq5xO6gqfTQoEMfvCg0a1qtWJv0"

bot = telebot.TeleBot(BOT_TOKEN)

# ====== معرف المشرف ======
ADMIN_ID = 8991420848

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

# ====== باقات البروكسي (بالدولار) ======
PROXY_PACKAGES = {
    "2 hours": {"points": 28, "usd": 0.28},
    "6 hours": {"points": 38, "usd": 0.38},
    "12 hours": {"points": 53, "usd": 0.53},
    "1 day": {"points": 93, "usd": 0.93},
    "2 days": {"points": 173, "usd": 1.73},
    "7 days": {"points": 503, "usd": 5.03},
    "10 days": {"points": 753, "usd": 7.53},
    "14 days": {"points": 1003, "usd": 10.03},
    "30 days": {"points": 1703, "usd": 17.03}
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

# ====== حسابات تليجرام ======
TELEGRAM_ACCOUNTS = {
    "🇮🇳 الهند ⚠️ SPAM - 0.25$": {"price": 0.25, "type": "SPAM"},
    "🇺🇸 أمريكا ⚠️ SPAM - 0.30$": {"price": 0.30, "type": "SPAM"},
    "🇲🇲 ميانمار ⚠️ SPAM - 0.30$": {"price": 0.30, "type": "SPAM"},
    "🇲🇦 المغرب - 0.60$": {"price": 0.60, "type": "Normal"},
}

# ====== أرقام واتساب ======
WHATSAPP_NUMBERS = {
    "🇵🇭 Philippines - 0.75$": {"price": 0.75, "number": "+639123456789"},
    "🇰🇭 Cambodia - 0.50$": {"price": 0.50, "number": "+85512345678"},
    "🇪🇪 Estonia - 1.10$": {"price": 1.10, "number": "+37251234567"},
    "🇨🇩 Congo - 0.35$": {"price": 0.35, "number": "+243812345678"},
    "🇹🇯 Tajikistan - 0.25$": {"price": 0.25, "number": "+992123456789"},
}

# ====== الأزرار الرئيسية ======
main_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
main_keyboard.add(
    KeyboardButton("🌐 احصل على بروكسي"),
    KeyboardButton("🎯 خدمات الرشق"),
    KeyboardButton("📱 حسابات تليجرام")
)
main_keyboard.add(
    KeyboardButton("💬 أرقام واتساب"),
    KeyboardButton("💰 شحن رصيد"),
    KeyboardButton("📋 حالة طلبي")
)
main_keyboard.add(
    KeyboardButton("📊 إحصائياتي"),
    KeyboardButton("🆘 الدعم"),
    KeyboardButton("ℹ️ عن البوت")
)

# ====== أزرار البروكسي ======
proxy_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
for country in PROXY_SERVERS.keys():
    proxy_keyboard.add(KeyboardButton(country))
proxy_keyboard.add(KeyboardButton("🔙 رجوع"))

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

# ====== أزرار حسابات تليجرام ======
telegram_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
for account in TELEGRAM_ACCOUNTS.keys():
    telegram_keyboard.add(KeyboardButton(account))
telegram_keyboard.add(KeyboardButton("🔙 رجوع"))

# ====== أزرار واتساب ======
whatsapp_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
for whatsapp in WHATSAPP_NUMBERS.keys():
    whatsapp_keyboard.add(KeyboardButton(whatsapp))
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

def send_activation_message(user_id, username, first_name, service_type, data, order_id):
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
                f"┃ 📱 البيانات: `{data.get('number', '')}`\n"
            )
        
        msg += f"┗━━━━━━━━━━━━━━━━━━━━━┛"
        
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
    balance = user_data.get("balance", 0) if user_data else 0
    balance_usd = balance * 0.01
    
    welcome_msg = (
        f"👋 أهلاً، {first_name}!\n"
        f"🆔 `{user_id}`\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 رصيدك: {balance_usd:.2f} USDT\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"✨ 💎 أهلاً بك في متجر الحسابات القوية!\n"
        f"حسابات تيليجرام موثوقة وجاهزة للاستخدام 🚀\n\n"
        f"اختر من القائمة أدناه 👇"
    )
    
    bot.send_message(
        message.chat.id,
        welcome_msg,
        parse_mode='Markdown',
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
        "📱 **حسابات تليجرام**\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "✨ حسابات موثوقة وجاهزة للاستخدام\n"
        "🚀 تسليم يدوي\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "اختر الدولة 👇",
        parse_mode='Markdown',
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
        "━━━━━━━━━━━━━━━━━━━━\n"
        "✨ أرقام مفعلة وجاهزة للاستخدام\n"
        "🚀 تسليم يدوي\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "اختر الدولة 👇",
        parse_mode='Markdown',
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
        "━━━━━━━━━━━━━━━━━━━━\n"
        "📌 **باقات الشحن:**\n\n"
        "┃ 💵 10$ = 100 نقطة\n"
        "┃ 💵 25$ = 275 نقطة (خصم 10%)\n"
        "┃ 💵 50$ = 600 نقطة (خصم 20%)\n"
        "┃ 💵 100$ = 1300 نقطة (خصم 30%)\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "📌 **طرق الدفع المتاحة:**\n\n"
        "• 🏦 تحويل بنكي\n"
        "• 📱 فودافون كاش\n"
        "• 💳 إنستا باي\n"
        "• 💵 باي بال\n"
        "• 🪙 USDT\n\n"
        "📞 **للشحن والتواصل:**\n"
        "[@PrimeSupport22](https://t.me/PrimeSupport22)",
        parse_mode='Markdown',
        reply_markup=payment_keyboard
    )

@bot.message_handler(commands=['balance'])
def balance_command(message):
    if not is_user_subscribed(message.from_user.id):
        start_command(message)
        return
    user_data = get_user_data(message.from_user.id)
    balance = user_data.get("balance", 0) if user_data else 0
    balance_usd = balance * 0.01
    
    bot.send_message(
        message.chat.id,
        f"📊 **إحصائياتك:**\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 رصيدك: {balance_usd:.2f} USDT\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📅 تاريخ التسجيل: {user_data.get('date', 'غير معروف') if user_data else 'غير معروف'}",
        reply_markup=main_keyboard
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
        "📦 الإصدار: 8.0\n"
        "🔄 يعمل 24/7\n\n"
        "✨ **الخدمات:**\n"
        "• 🌐 بروكسي - 5 دول - 17 سيرفر\n"
        "• 🎯 خدمات الرشق\n"
        "• 📱 حسابات تليجرام\n"
        "• 💬 أرقام واتساب\n\n"
        "💰 نظام نقاط للشحن\n"
        "🔄 تسليم يدوي لجميع الخدمات",
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

@bot.message_handler(func=lambda message: message.text == "📱 حسابات تليجرام")
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

@bot.message_handler(func=lambda message: message.text == "🆘 الدعم")
def support_button(message):
    support_msg = (
        "🆘 **مركز الدعم**\n\n"
        "📌 **طرق التواصل:**\n"
        "• 📢 قناة الدعم: [@PrimeSupport22](https://t.me/PrimeSupport22)\n"
        "• 💬 أرسل رسالتك هنا وسيتم الرد خلال 24 ساعة\n\n"
        "📋 **للاستفسار، أرسل:**\n"
        "• رقم الطلب\n"
        "• شرح المشكلة\n"
        "• صورة توضيحية\n\n"
        "⏰ أوقات العمل: 9 صباحاً - 12 منتصف الليل"
    )
    
    bot.send_message(
        message.chat.id,
        support_msg,
        parse_mode='Markdown',
        reply_markup=main_keyboard
    )

@bot.message_handler(func=lambda message: message.text == "ℹ️ عن البوت")
def about_button(message):
    about_command(message)

# ============================================
# ====== شراء حسابات تليجرام ======
# ============================================

def process_telegram_order(message, account_key):
    user_id = message.from_user.id
    account_data = TELEGRAM_ACCOUNTS.get(account_key, {})
    price = account_data.get("price", 0)
    country = account_key.split(" - ")[0]
    
    # التحقق من الرصيد
    user_data = get_user_data(user_id)
    balance = user_data.get("balance", 0) if user_data else 0
    balance_usd = balance * 0.01
    
    if balance_usd < price:
        bot.send_message(
            message.chat.id,
            f"❌ **رصيد غير كافٍ!**\n\n"
            f"💰 رصيدك: {balance_usd:.2f}$\n"
            f"💳 المطلوب: {price:.2f}$\n\n"
            "📌 اضغط: 💰 شحن رصيد",
            reply_markup=main_keyboard
        )
        return
    
    # إنشاء طلب
    order_id = generate_order_id()
    orders = load_orders()
    orders.append({
        "order_id": order_id,
        "user_id": user_id,
        "service_type": "حساب تليجرام",
        "country": country,
        "price": price,
        "status": "⏳ قيد التجهيز (يدوي)",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_orders(orders)
    
    # خصم الرصيد
    points_needed = int(price * 100)
    user_data["balance"] = balance - points_needed
    save_data(load_data())
    
    # إشعار للمشرف
    admin_msg = (
        f"🛒 **طلب حساب تليجرام جديد**\n\n"
        f"┏━━━━━━━━━━━━━━━━━━━━━┓\n"
        f"┃ 📋 رقم الطلب: `{order_id}`\n"
        f"┃ 👤 المستخدم: {message.from_user.first_name}\n"
        f"┃ 🆔 المعرف: `{user_id}`\n"
        f"┃ 📛 اليوزر: @{message.from_user.username or 'لا يوجد'}\n"
        f"┃ 🌍 الدولة: {country}\n"
        f"┃ 💰 السعر: {price:.2f}$\n"
        f"┃ 📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        "📌 **يرجى تجهيز الحساب وإرساله للمستخدم**"
    )
    
    bot.send_message(ADMIN_ID, admin_msg, parse_mode='Markdown')
    
    # رسالة للمستخدم
    bot.send_message(
        message.chat.id,
        f"✅ **تم استلام طلب حساب تليجرام!**\n\n"
        f"┏━━━━━━━━━━━━━━━━━━━━━┓\n"
        f"┃ 📋 رقم الطلب: `{order_id}`\n"
        f"┃ 🌍 الدولة: {country}\n"
        f"┃ 💰 السعر: {price:.2f}$\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        "⏳ **جاري تجهيز الحساب...**\n"
        "📌 سيتم إرسال بيانات الحساب خلال 24 ساعة.\n\n"
        "📞 **للحصول على الحساب فوراً:**\n"
        "• راسل الدعم: [@PrimeSupport22](https://t.me/PrimeSupport22)\n\n"
        f"💰 تم خصم {price:.2f}$ من رصيدك",
        parse_mode='Markdown',
        reply_markup=main_keyboard
    )

@bot.message_handler(func=lambda message: message.text in TELEGRAM_ACCOUNTS.keys())
def buy_telegram_account(message):
    process_telegram_order(message, message.text)

# ============================================
# ====== شراء أرقام واتساب ======
# ============================================

def process_whatsapp_order(message, whatsapp_key):
    user_id = message.from_user.id
    whatsapp_data = WHATSAPP_NUMBERS.get(whatsapp_key, {})
    price = whatsapp_data.get("price", 0)
    number = whatsapp_data.get("number", "")
    country = whatsapp_key.split(" - ")[0]
    
    # التحقق من الرصيد
    user_data = get_user_data(user_id)
    balance = user_data.get("balance", 0) if user_data else 0
    balance_usd = balance * 0.01
    
    if balance_usd < price:
        bot.send_message(
            message.chat.id,
            f"❌ **رصيد غير كافٍ!**\n\n"
            f"💰 رصيدك: {balance_usd:.2f}$\n"
            f"💳 المطلوب: {price:.2f}$\n\n"
            "📌 اضغط: 💰 شحن رصيد",
            reply_markup=main_keyboard
        )
        return
    
    # إنشاء طلب
    order_id = generate_order_id()
    orders = load_orders()
    orders.append({
        "order_id": order_id,
        "user_id": user_id,
        "service_type": "رقم واتساب",
        "country": country,
        "number": number,
        "price": price,
        "status": "⏳ قيد التجهيز (يدوي)",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_orders(orders)
    
    # خصم الرصيد
    points_needed = int(price * 100)
    user_data["balance"] = balance - points_needed
    save_data(load_data())
    
    # إشعار للمشرف
    admin_msg = (
        f"🛒 **طلب رقم واتساب جديد**\n\n"
        f"┏━━━━━━━━━━━━━━━━━━━━━┓\n"
        f"┃ 📋 رقم الطلب: `{order_id}`\n"
        f"┃ 👤 المستخدم: {message.from_user.first_name}\n"
        f"┃ 🆔 المعرف: `{user_id}`\n"
        f"┃ 📛 اليوزر: @{message.from_user.username or 'لا يوجد'}\n"
        f"┃ 🌍 الدولة: {country}\n"
        f"┃ 📱 الرقم: `{number}`\n"
        f"┃ 💰 السعر: {price:.2f}$\n"
        f"┃ 📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        "📌 **يرجى تجهيز الرقم وإرساله للمستخدم**"
    )
    
    bot.send_message(ADMIN_ID, admin_msg, parse_mode='Markdown')
    
    # رسالة للمستخدم
    bot.send_message(
        message.chat.id,
        f"✅ **تم استلام طلب رقم واتساب!**\n\n"
        f"┏━━━━━━━━━━━━━━━━━━━━━┓\n"
        f"┃ 📋 رقم الطلب: `{order_id}`\n"
        f"┃ 🌍 الدولة: {country}\n"
        f"┃ 📱 الرقم: `{number}`\n"
        f"┃ 💰 السعر: {price:.2f}$\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        "⏳ **جاري تجهيز الرقم...**\n"
        "📌 سيتم إرسال الرقم خلال 24 ساعة.\n\n"
        "📞 **للحصول على الرقم فوراً:**\n"
        "• راسل الدعم: [@PrimeSupport22](https://t.me/PrimeSupport22)\n\n"
        f"💰 تم خصم {price:.2f}$ من رصيدك",
        parse_mode='Markdown',
        reply_markup=main_keyboard
    )

@bot.message_handler(func=lambda message: message.text in WHATSAPP_NUMBERS.keys())
def buy_whatsapp_number(message):
    process_whatsapp_order(message, message.text)

# ============================================
# ====== اختيار دولة البروكسي ======
# ============================================

@bot.message_handler(func=lambda message: message.text in PROXY_SERVERS.keys())
def select_proxy_country(message):
    user_id = message.from_user.id
    country = message.text
    
    if user_id not in user_temp_data:
        user_temp_data[user_id] = {}
    user_temp_data[user_id]["country"] = country
    
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
    
    if user_id not in user_temp_data:
        user_temp_data[user_id] = {}
    user_temp_data[user_id]["server"] = server
    
    bot.send_message(
        message.chat.id,
        f"🖥️ **السيرفر: {server}**\n\n"
        "⏱ اختر المدة المطلوبة:\n\n"
        "2 hours - 0.28$\n"
        "6 hours - 0.38$\n"
        "12 hours - 0.53$\n"
        "1 day - 0.93$\n"
        "2 days - 1.73$\n"
        "7 days - 5.03$\n"
        "10 days - 7.53$\n"
        "14 days - 10.03$\n"
        "30 days - 17.03$",
        reply_markup=duration_keyboard
    )

# ============================================
# ====== اختيار مدة البروكسي ======
# ============================================

@bot.message_handler(func=lambda message: message.text in PROXY_PACKAGES.keys())
def select_proxy_duration(message):
    user_id = message.from_user.id
    duration = message.text
    
    if user_id not in user_temp_data:
        user_temp_data[user_id] = {}
    user_temp_data[user_id]["duration"] = duration
    
    package = PROXY_PACKAGES[duration]
    
    bot.send_message(
        message.chat.id,
        f"⏱ **المدة: {duration}**\n"
        f"💰 السعر: {package['usd']:.2f}$\n\n"
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
    
    if user_id not in user_temp_data:
        user_temp_data[user_id] = {}
    user_temp_data[user_id]["protocol"] = protocol
    
    bot.send_message(
        message.chat.id,
        f"🔒 **البروتوكول: {protocol}**\n\n"
        "👤 **أرسل اسم المستخدم المطلوب:**"
    )

# ============================================
# ====== استقبال اسم المستخدم ======
# ============================================

@bot.message_handler(func=lambda message: re.match(r'^[a-zA-Z0-9_]{3,20}$', message.text) and message.text not in ["🔙 رجوع", "🌐 احصل على بروكسي", "🎯 خدمات الرشق", "📱 حسابات تليجرام", "💬 أرقام واتساب", "💰 شحن رصيد", "📋 حالة طلبي", "📊 إحصائياتي", "🆘 الدعم", "ℹ️ عن البوت"])
def get_proxy_username(message):
    user_id = message.from_user.id
    username_input = message.text
    
    if user_id not in user_temp_data or "country" not in user_temp_data[user_id]:
        bot.send_message(message.chat.id, "⚠️ حدث خطأ، ابدأ من جديد /proxy")
        return
    
    user_temp_data[user_id]["username"] = username_input
    
    bot.send_message(
        message.chat.id,
        f"👤 **اسم المستخدم: {username_input}**\n\n"
        "🔑 **أرسل كلمة المرور المطلوبة:**"
    )

# ============================================
# ====== استقبال كلمة المرور ======
# ============================================

@bot.message_handler(func=lambda message: len(message.text) >= 4 and message.text not in ["🔙 رجوع", "🌐 احصل على بروكسي", "🎯 خدمات الرشق", "📱 حسابات تليجرام", "💬 أرقام واتساب", "💰 شحن رصيد", "📋 حالة طلبي", "📊 إحصائياتي", "🆘 الدعم", "ℹ️ عن البوت"])
def get_proxy_password(message):
    user_id = message.from_user.id
    password_input = message.text
    
    if user_id not in user_temp_data or "username" not in user_temp_data[user_id]:
        bot.send_message(message.chat.id, "⚠️ حدث خطأ، ابدأ من جديد /proxy")
        return
    
    user_temp_data[user_id]["password"] = password_input
    
    data = user_temp_data[user_id]
    duration = data.get("duration", "1 day")
    package = PROXY_PACKAGES.get(duration, {"points": 93, "usd": 0.93})
    price_usd = package["usd"]
    price_points = package["points"]
    
    # التحقق من الرصيد
    user_data = get_user_data(user_id)
    balance = user_data.get("balance", 0) if user_data else 0
    balance_usd = balance * 0.01
    
    if balance_usd < price_usd:
        bot.send_message(
            message.chat.id,
            f"❌ **رصيد غير كافٍ!**\n\n"
            f"💰 رصيدك: {balance_usd:.2f}$\n"
            f"💳 المطلوب: {price_usd:.2f}$\n\n"
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
        duration
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
        "duration": duration,
        "protocol": data.get("protocol", ""),
        "ip": proxy_data["ip"],
        "port": proxy_data["port"],
        "username": data.get("username", ""),
        "password": data.get("password", ""),
        "expiry": proxy_data["expiry"],
        "price_usd": price_usd,
        "price_points": price_points,
        "status": "⏳ قيد التجهيز (يدوي)",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_orders(orders)
    
    # خصم الرصيد
    user_data["balance"] = balance - price_points
    save_data(load_data())
    
    # إشعار للمشرف
    admin_msg = (
        f"🛒 **طلب بروكسي جديد**\n\n"
        f"┏━━━━━━━━━━━━━━━━━━━━━┓\n"
        f"┃ 📋 رقم الطلب: `{order_id}`\n"
        f"┃ 👤 المستخدم: {message.from_user.first_name}\n"
        f"┃ 🆔 المعرف: `{user_id}`\n"
        f"┃ 📛 اليوزر: @{message.from_user.username or 'لا يوجد'}\n"
        f"┃ 🌍 الدولة: {data.get('country', '')}\n"
        f"┃ 🖥️ السيرفر: {data.get('server', '')}\n"
        f"┃ ⏱ المدة: {duration}\n"
        f"┃ 🔒 البروتوكول: {data.get('protocol', '')}\n"
        f"┃ 👤 Username: {data.get('username', '')}\n"
        f"┃ 🔑 Password: {data.get('password', '')}\n"
        f"┃ 💰 السعر: {price_usd:.2f}$\n"
        f"┃ 📅 التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        "📌 **يرجى تجهيز البروكسي وإرساله للمستخدم**"
    )
    
    bot.send_message(ADMIN_ID, admin_msg, parse_mode='Markdown')
    
    # رسالة للمستخدم
    bot.send_message(
        message.chat.id,
        f"✅ **تم استلام طلب البروكسي!**\n\n"
        f"┏━━━━━━━━━━━━━━━━━━━━━┓\n"
        f"┃ 📋 رقم الطلب: `{order_id}`\n"
        f"┃ 🌍 الدولة: {data.get('country', '')}\n"
        f"┃ 🖥️ السيرفر: {data.get('server', '')}\n"
        f"┃ ⏱ المدة: {duration}\n"
        f"┃ 🔒 البروتوكول: {data.get('protocol', '')}\n"
        f"┃ 💰 السعر: {price_usd:.2f}$\n"
        f"┗━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        "⏳ **جاري تجهيز البروكسي...**\n"
        "📌 سيتم إرسال بيانات البروكسي خلال 24 ساعة.\n\n"
        "📞 **للحصول على البروكسي فوراً:**\n"
        "• راسل الدعم: [@PrimeSupport22](https://t.me/PrimeSupport22)\n\n"
        f"💰 تم خصم {price_usd:.2f}$ من رصيدك",
        parse_mode='Markdown',
        reply_markup=main_keyboard
    )
    
    # إرسال نسخة لقناة التفعيلات
    send_activation_message(
        user_id,
        message.from_user.username or "لا يوجد",
        message.from_user.first_name,
        "بروكسي",
        proxy_data,
        order_id
    )
    
    # حذف البيانات المؤقتة
    if user_id in user_temp_data:
        del user_temp_data[user_id]

# ============================================
# ====== خدمات الرشق ======
# ============================================

@bot.message_handler(func=lambda message: message.text in ["📱 رشق تليجرام", "💬 رشق واتساب", "📸 رشق إنستغرام", "🐦 رشق تويتر", "🎯 رشق مخصص"])
def rashq_services(message):
    rashq_info = {
        "📱 رشق تليجرام": {"price": "3$", "amount": "1000 متابع", "time": "3 أيام"},
        "💬 رشق واتساب": {"price": "4$", "amount": "500 متابع", "time": "5 أيام"},
        "📸 رشق إنستغرام": {"price": "5$", "amount": "500 متابع", "time": "7 أيام"},
        "🐦 رشق تويتر": {"price": "4.5$", "amount": "500 متابع", "time": "5 أيام"},
        "🎯 رشق مخصص": {"price": "حسب الطلب", "amount": "حسب الطلب", "time": "حسب الطلب"}
    }
    
    info = rashq_info.get(message.text, {})
    
    bot.send_message(
        message.chat.id,
        f"🎯 **{message.text}**\n\n"
        f"💰 السعر: {info.get('price', '')}\n"
        f"👥 الكمية: {info.get('amount', '')}\n"
        f"⏱ المدة: {info.get('time', '')}\n\n"
        "📌 للطلب: تواصل مع الدعم\n"
        "📞 [@PrimeSupport22](https://t.me/PrimeSupport22)",
        parse_mode='Markdown',
        reply_markup=rashq_keyboard
    )

# ============================================
# ====== طرق الدفع ======
# ============================================

@bot.message_handler(func=lambda message: message.text in ["🏦 تحويل بنكي", "📱 فودافون كاش", "💳 إنستا باي", "💵 باي بال", "🪙 USDT"])
def payment_methods(message):
    payment_info = {
        "🏦 تحويل بنكي": "البنك الأهلي - حساب: 1234567890",
        "📱 فودافون كاش": "0123456789 - Ahmed Mohamed",
        "💳 إنستا باي": "0123456789 - البنك الأهلي",
        "💵 باي بال": "paypal@example.com",
        "🪙 USDT": "TRC20: TYourWalletAddressHere"
    }
    
    bot.send_message(
        message.chat.id,
        f"💳 **{message.text}**\n\n"
        f"📌 {payment_info.get(message.text, '')}\n\n"
        "💰 **باقات الشحن:**\n"
        "10$ = 100 نقطة\n"
        "25$ = 275 نقطة (خصم 10%)\n"
        "50$ = 600 نقطة (خصم 20%)\n"
        "100$ = 1300 نقطة (خصم 30%)\n\n"
        "📌 بعد الدفع، أرسل إيصال الدفع هنا\n"
        "📞 للتواصل: [@PrimeSupport22](https://t.me/PrimeSupport22)",
        parse_mode='Markdown',
        reply_markup=payment_keyboard
    )

# ============================================
# ====== زر الرجوع ======
# ============================================

@bot.message_handler(func=lambda message: message.text == "🔙 رجوع")
def back_button(message):
    start_command(message)

# ============================================
# ====== أوامر المشرف ======
# ============================================

@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ غير مصرح لك")
        return
    
    users = get_users_count()
    orders = load_orders()
    total_orders = len(orders)
    pending = [o for o in orders if o.get("status") == "⏳ قيد التجهيز (يدوي)"]
    pending_count = len(pending)
    
    admin_msg = (
        "🔐 **لوحة تحكم المشرف**\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 **الإحصائيات:**\n"
        f"┃ 👥 المستخدمين: {users}\n"
        f"┃ 📦 إجمالي الطلبات: {total_orders}\n"
        f"┃ ⏳ طلبات معلقة: {pending_count}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        "📌 **الأوامر المتاحة:**\n\n"
        "┃ /pending - عرض الطلبات المعلقة\n"
        "┃ /orders - عرض جميع الطلبات\n"
        "┃ /users - عرض المستخدمين\n"
        "┃ /stats - إحصائيات مفصلة\n"
        "┃ /broadcast - إرسال رسالة للجميع\n\n"
        "📌 **أوامر التسليم:**\n\n"
        "┃ /deliver ORD-xxx IP Port Protocol User Pass\n"
        "┃ /deliver_account ORD-xxx number password\n"
        "┃ /deliver_whatsapp ORD-xxx number password\n\n"
        f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    
    bot.send_message(message.chat.id, admin_msg, parse_mode='Markdown')

@bot.message_handler(commands=['pending'])
def pending_orders(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ غير مصرح لك")
        return
    
    orders = load_orders()
    pending = [o for o in orders if o.get("status") == "⏳ قيد التجهيز (يدوي)"]
    
    if not pending:
        bot.reply_to(message, "📋 لا توجد طلبات معلقة ✅")
        return
    
    msg = "⏳ **الطلبات المعلقة:**\n\n"
    for order in pending:
        msg += (
            f"┏━━━━━━━━━━━━━━━━━━━━━┓\n"
            f"┃ 📋 {order['order_id']}\n"
            f"┃ 🎯 {order.get('service_type', '')}\n"
            f"┃ 👤 {order.get('first_name', 'غير معروف')}\n"
            f"┃ 🆔 {order.get('user_id', '')}\n"
            f"┃ 🌍 {order.get('country', '')}\n"
            f"┃ 📅 {order.get('date', '')}\n"
            f"┗━━━━━━━━━━━━━━━━━━━━━┛\n\n"
        )
    
    msg += "\n📌 **للتسليم استخدم:**\n"
    msg += "• /deliver ORD-xxx IP Port Protocol User Pass (بروكسي)\n"
    msg += "• /deliver_account ORD-xxx number password (حساب تليجرام)\n"
    msg += "• /deliver_whatsapp ORD-xxx number password (واتساب)"
    
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['orders'])
def all_orders(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ غير مصرح لك")
        return
    
    orders = load_orders()
    
    if not orders:
        bot.reply_to(message, "📋 لا توجد طلبات")
        return
    
    total = len(orders)
    pending = len([o for o in orders if o.get("status") == "⏳ قيد التجهيز (يدوي)"])
    delivered = len([o for o in orders if o.get("status") == "✅ تم التسليم"])
    
    msg = (
        f"📦 **جميع الطلبات:**\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"┃ 📊 الإجمالي: {total}\n"
        f"┃ ⏳ معلق: {pending}\n"
        f"┃ ✅ تم التسليم: {delivered}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
    )
    
    for order in orders[-10:]:
        msg += (
            f"┃ {order['order_id']}\n"
            f"┃ 🎯 {order.get('service_type', '')}\n"
            f"┃ 📌 {order.get('status', '')}\n"
            f"┃ ─────────────────\n"
        )
    
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['users'])
def users_list(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ غير مصرح لك")
        return
    
    data = load_data()
    users = data.get("users", [])
    count = len(users)
    
    msg = f"👥 **المستخدمين:** {count}\n\n"
    
    if users:
        for user in users[-10:]:
            msg += (
                f"┃ 👤 {user.get('first_name', '')}\n"
                f"┃ 🆔 {user.get('id', '')}\n"
                f"┃ 📅 {user.get('date', '')}\n"
                f"┃ ─────────────────\n"
            )
    
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['stats'])
def stats_command(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ غير مصرح لك")
        return
    
    data = load_data()
    orders = load_orders()
    
    users = len(data.get("users", []))
    total_orders = len(orders)
    pending = len([o for o in orders if o.get("status") == "⏳ قيد التجهيز (يدوي)"])
    delivered = len([o for o in orders if o.get("status") == "✅ تم التسليم"])
    
    total_balance = sum([user.get("balance", 0) for user in data.get("users", [])])
    
    msg = (
        f"📊 **إحصائيات البوت:**\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 **المستخدمين:**\n"
        f"┃ الإجمالي: {users}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📦 **الطلبات:**\n"
        f"┃ الإجمالي: {total_orders}\n"
        f"┃ ⏳ معلق: {pending}\n"
        f"┃ ✅ تم التسليم: {delivered}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💰 **النقاط:**\n"
        f"┃ إجمالي النقاط: {total_balance}\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    
    bot.send_message(message.chat.id, msg)

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ غير مصرح لك")
        return
    
    text = message.text.replace("/broadcast", "").strip()
    
    if not text:
        bot.reply_to(message, "⚠️ استخدم: /broadcast نص الرسالة")
        return
    
    data = load_data()
    users = data.get("users", [])
    success = 0
    fail = 0
    
    bot.reply_to(message, f"⏳ جاري إرسال الرسالة لـ {len(users)} مستخدم...")
    
    for user in users:
        try:
            bot.send_message(
                user["id"],
                f"📢 **إعلان من الإدارة**\n\n{text}",
                parse_mode='Markdown'
            )
            success += 1
        except:
            fail += 1
    
    bot.send_message(
        message.chat.id,
        f"✅ **تم الإرسال!**\n\n"
        f"┃ ✅ نجح: {success}\n"
        f"┃ ❌ فشل: {fail}\n"
        f"┃ 👥 الإجمالي: {len(users)}"
    )

# ============================================
# ====== أوامر التسليم (للمشرف) ======
# ============================================

@bot.message_handler(commands=['deliver'])
def deliver_proxy(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ غير مصرح لك")
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 7:
            bot.reply_to(message, "⚠️ استخدم: /deliver ORD-xxx IP Port Protocol User Pass")
            return
        
        order_id = parts[1]
        ip = parts[2]
        port = parts[3]
        protocol = parts[4]
        username = parts[5]
        password = parts[6]
        
        orders = load_orders()
        for order in orders:
            if order["order_id"] == order_id:
                user_id = order["user_id"]
                
                bot.send_message(
                    user_id,
                    f"✅ **تم تجهيز البروكسي!**\n\n"
                    f"┏━━━━━━━━━━━━━━━━━━━━━┓\n"
                    f"┃ 📋 رقم الطلب: `{order_id}`\n"
                    f"┃ 🌍 الدولة: {order.get('country', '')}\n"
                    f"┃ 🌐 IP: `{ip}`\n"
                    f"┃ 🔢 Port: `{port}`\n"
                    f"┃ 🔒 البروتوكول: {protocol}\n"
                    f"┃ 👤 Username: `{username}`\n"
                    f"┃ 🔑 Password: `{password}`\n"
                    f"┗━━━━━━━━━━━━━━━━━━━━━┛\n\n"
                    "🎉 **تم التسليم!**\n"
                    "📌 يمكنك استخدام البروكسي فوراً\n\n"
                    "📞 للاستفسار: [@PrimeSupport22](https://t.me/PrimeSupport22)",
                    parse_mode='Markdown'
                )
                
                order["status"] = "✅ تم التسليم"
                order["ip"] = ip
                order["port"] = port
                order["delivered_protocol"] = protocol
                order["delivered_username"] = username
                order["delivered_password"] = password
                save_orders(orders)
                
                bot.reply_to(message, f"✅ تم تسليم البروكسي {order_id} للمستخدم")
                return
        
        bot.reply_to(message, f"❌ الطلب {order_id} غير موجود")
    except Exception as e:
        bot.reply_to(message, f"⚠️ حدث خطأ: {e}")

@bot.message_handler(commands=['deliver_account'])
def deliver_account(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ غير مصرح لك")
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 4:
            bot.reply_to(message, "⚠️ استخدم: /deliver_account ORD-xxx number password")
            return
        
        order_id = parts[1]
        number = parts[2]
        password = parts[3]
        
        orders = load_orders()
        for order in orders:
            if order["order_id"] == order_id:
                user_id = order["user_id"]
                
                bot.send_message(
                    user_id,
                    f"✅ **تم تجهيز حساب تليجرام!**\n\n"
                    f"┏━━━━━━━━━━━━━━━━━━━━━┓\n"
                    f"┃ 📋 رقم الطلب: `{order_id}`\n"
                    f"┃ 🌍 الدولة: {order.get('country', '')}\n"
                    f"┃ 📱 الرقم: `{number}`\n"
                    f"┃ 🔑 كلمة المرور: `{password}`\n"
                    f"┗━━━━━━━━━━━━━━━━━━━━━┛\n\n"
                    "🎉 **تم التسليم!**\n"
                    "📌 يمكنك استخدام الحساب فوراً\n\n"
                    "📞 للاستفسار: [@PrimeSupport22](https://t.me/PrimeSupport22)",
                    parse_mode='Markdown'
                )
                
                order["status"] = "✅ تم التسليم"
                order["delivered_number"] = number
                order["delivered_password"] = password
                save_orders(orders)
                
                bot.reply_to(message, f"✅ تم تسليم الحساب {order_id} للمستخدم")
                return
        
        bot.reply_to(message, f"❌ الطلب {order_id} غير موجود")
    except Exception as e:
        bot.reply_to(message, f"⚠️ حدث خطأ: {e}")

@bot.message_handler(commands=['deliver_whatsapp'])
def deliver_whatsapp(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ غير مصرح لك")
        return
    
    try:
        parts = message.text.split()
        if len(parts) < 4:
            bot.reply_to(message, "⚠️ استخدم: /deliver_whatsapp ORD-xxx number password")
            return
        
        order_id = parts[1]
        number = parts[2]
        password = parts[3]
        
        orders = load_orders()
        for order in orders:
            if order["order_id"] == order_id:
                user_id = order["user_id"]
                
                bot.send_message(
                    user_id,
                    f"✅ **تم تجهيز رقم واتساب!**\n\n"
                    f"┏━━━━━━━━━━━━━━━━━━━━━┓\n"
                    f"┃ 📋 رقم الطلب: `{order_id}`\n"
                    f"┃ 🌍 الدولة: {order.get('country', '')}\n"
                    f"┃ 📱 الرقم: `{number}`\n"
                    f"┃ 🔑 كلمة المرور: `{password}`\n"
                    f"┗━━━━━━━━━━━━━━━━━━━━━┛\n\n"
                    "🎉 **تم التسليم!**\n"
                    "📌 يمكنك استخدام الرقم فوراً\n\n"
                    "📞 للاستفسار: [@PrimeSupport22](https://t.me/PrimeSupport22)",
                    parse_mode='Markdown'
                )
                
                order["status"] = "✅ تم التسليم"
                order["delivered_number"] = number
                order["delivered_password"] = password
                save_orders(orders)
                
                bot.reply_to(message, f"✅ تم تسليم رقم واتساب {order_id} للمستخدم")
                return
        
        bot.reply_to(message, f"❌ الطلب {order_id} غير موجود")
    except Exception as e:
        bot.reply_to(message, f"⚠️ حدث خطأ: {e}")

# ============================================
# ====== تشغيل البوت ======
# ============================================

if __name__ == "__main__":
    print("🚀 البوت شغال...")
    print("🌐 5 دول - 17 سيرفر بروكسي")
    print("📱 حسابات تليجرام: الهند، أمريكا، ميانمار، المغرب")
    print("💬 أرقام واتساب: Philippines, Cambodia, Estonia, Congo, Tajikistan")
    print("👤 المشرف:", ADMIN_ID)
    print("📅", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("=" * 40)
    
    try:
        bot.remove_webhook()
    except:
        pass
    
    bot.infinity_polling()
