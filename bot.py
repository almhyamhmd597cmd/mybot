import telebot
import sqlite3
from telebot import types

API_TOKEN = '8719748870:AAHH299k9YJipw8q7NKMURXbAFvCF-vvdaY' # توكن البوت الذي أرسلته
ADMIN_ID = 870561734  # معرف الأدمن الخاص بك

bot = telebot.TeleBot(API_TOKEN)

# إنشاء قاعدة البيانات وجدول المستخدمين
def init_db():
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            referrer_id INTEGER,
            referrals_count INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# دالة التحقق من الصلاحيات (الأدمن أو من وصل 100 دعوة)
def has_access(user_id):
    if user_id == ADMIN_ID:
        return True
    
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT referrals_count FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row and row[0] >= 100:
        return True
    return False

# أمر البداية مع الأزرار الشاملة ورابط الدعوة
@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    text_args = message.text.split()
    
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user_exists = cursor.fetchone()
    
    if not user_exists:
        referrer_id = None
        if len(text_args) > 1:
            try:
                referrer_id = int(text_args[1])
                if referrer_id != user_id:
                    cursor.execute('UPDATE users SET referrals_count = referrals_count + 1 WHERE user_id = ?', (referrer_id,))
                    bot.send_message(referrer_id, f"🎉 دخل عضو جديد عبر رابط دعوتك!")
            except ValueError:
                pass
        
        cursor.execute('INSERT INTO users (user_id, referrer_id) VALUES (?, ?)', (user_id, referrer_id))
        conn.commit()
    
    conn.close()
    
    bot_info = bot.get_me()
    invite_link = f"https://t.me/{bot_info.username}?start={user_id}"
    
    # تصميم الأزرار كاملة
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('شراء نسخة البوت 🛒', 'شروط الاستخدام 📜')
    markup.row('قناة المطور ↗️', 'تواصل مع المطور 📞')
    markup.row('اختراق Kwai 🎥', 'اختراق Telegram ✉️')
    markup.row('اختراق Likee ❤️', 'اختراق Messenger 💬')
    markup.row('بحث في GitHub 🔍', 'معلومات تيك توك 🎵')
    markup.row('معلومات انستجرام 📷', 'سحب ملفات الهاتف 📁')
    markup.row('توليد صورة (AI) 🎨', 'تحميل فيديوهات السوشيال 📥')
    markup.row('بلاغات تيك توك ⛔', 'سحب الحافظة 📋')
    markup.row('تحويل الصورة لرابط 📥', 'Google Gemini 👽')
    markup.row('أدوات المعرفات (ID) 🆔', 'شكر خاص ❤️')
    markup.row('صيد يوزرت تلجرام 🔍', 'الرقام وهمية ☎️')
    markup.row('🌍 قسم الأرقام الوهمية العربية 📱')
    markup.row('رابط دردشة سريع 📞', 'نصائح وتوعية 🛡️')
    markup.row('اغلاق المواقع 🔒', 'كيف تصبح هاكر 👨‍💻')
    markup.row('تجمع نقاط 💰', 'هدية النقاط 🎁')
    markup.row('اختراق يوتيوب 🔴', 'اختراق تويتر X 💀')
    markup.row('اختراق حساب جوجل G', 'معرفة رقم الضحية 📱')
    markup.row('🔴 اختراق الهاتف كاملاً VIP ! 📱')
    markup.row('تحويل النص إلى صوت 🎙️', 'زخرفة نصوص ✨')
    markup.row('اختصار الروابط 🔗', 'تكرار النص 🔄')
    markup.row('توليد كلمة سر 🔑', 'ترجمة 🌐')
    markup.row('انشاء فيروس 🦠', 'اعطني نكته 😂')
    markup.row('تشفير ملفات بايثون 🐍', 'اتصال الاي رقم 📞')
    markup.row('إنشاء بريد وهمي 📧', 'تشفير HTML 🌐')
    markup.row('معلومات IP | 📱', 'كشف حساب بـ ID 🔍')
    markup.row('شرح استخدام البوت 📖', 'فحص روابط 🔍')
    markup.row('إنشاء باركود ⬛', 'قراءة باركود 📁')
    markup.row('تلغيم رابط 💣', 'استخراج صورة يوتيوب 🎬')
    markup.row('فيزات وهمية 💳', 'IDBot 🤖')
    markup.row('تلقيم صوره 💀', 'اختراق كاميرا ام وخ 📸')
    markup.row('تسجيل صوت الضحية 🎙️', 'تصوير الضحية فيديو 📹')
    markup.row('تحديد الموقع الجغرافي 📍', 'مسابقة الحلم 2026 🎁')
    markup.row('لعبة الأذكياء (أسئلة) 🧠', 'اختراق انستجرام 🚀')
    markup.row('اختراق تيك توك 🎬', 'اختراق واتساب ✅')
    markup.row('اختراق فيسبوك 🔵', 'اختراق بيجي 🔥')
    markup.row('اختراق سناب شات 👻', 'الذكاء الاصطناعي 🤖')
    markup.row('شحن جواهر فري فاير 💎', 'سحب أرباح ليمو 💰')
    markup.row('تحويل بالذكاء الاصطناعي')

    welcome_text = (
        "مرحباً بك في البوت الشامل! 👋\n\n"
        "✨ الخدمات المجانية متاحة للجميع.\n"
        "🔒 الخدمات المقفلة تتطلب دعوة 100 شخص.\n\n"
        f"🔗 رابط الدعوة الخاص بك:\n{invite_link}"
    )
    bot.reply_to(message, welcome_text, reply_markup=markup)

# زر فحص النقاط
@bot.message_handler(commands=['my_points'])
def check_points(message):
    user_id = message.from_user.id
    conn = sqlite3.connect('bot_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT referrals_count FROM users WHERE user_id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    
    count = row[0] if row else 0
    bot.reply_to(message, f"📊 عدد الأشخاص الذين دعوتهم هو: {count} شخصاً.")

# معالجة الضغط على أي زر من القائمة
@bot.message_handler(func=lambda message: True)
def handle_all_buttons(message):
    user_id = message.from_user.id
    text = message.text
    
    # يمكنك تخصيص الردود هنا حسب الزر المضغوط
    if text == 'شروط الاستخدام 📜':
        bot.reply_to(message, "📜 شروط الاستخدام: ممنوع استخدام الخدمات فيما يغضب الله.")
    elif text == 'تجمع نقاط 💰':
        bot_info = bot.get_me()
        invite_link = f"https://t.me/{bot_info.username}?start={user_id}"
        bot.reply_to(message, f"💰 لجمع النقاط، قم بنشر رابط دعوتك:\n{invite_link}")
    else:
        # فحص الحماية للخدمات الأخرى
        if not has_access(user_id):
            bot.reply_to(message, "🔒 عذراً، هذا القسم مقفل ويتطلب منك دعوة 100 شخص لفتح جميع الخدمات تلقائياً! استخدم /my_points لمعرفة عدد دعواتك.")
        else:
            bot.reply_to(message, f"✅ تم تفعيل خدمة ({text}) لأنك تمتلك الصلاحيات الكاملة!")

if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()
