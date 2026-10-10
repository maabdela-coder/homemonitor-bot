import telebot
from telebot import types
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# 1. Render የሚጠብቀውን ፖርት ለማሟላት የሚረዳ አጭር ዌብ ሰርቨር (Dummy Web Server)
def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    class SimpleHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Home Monitor Bot is running 24/7!")
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# ሰርቨሩን በጀርባ (Background) ማስጀመር
threading.Thread(target=run_dummy_server, daemon=True).start()

# የቦቱን ቶከን እና የአድሚን ዩዘር ID እዚህ ያስገቡ
TOKEN = '8701815004:AAF0hU6MCU0HvuaWdtmuEy9P1k_wj5FptLA'
ADMIN_ID = 602130279  # ቁጥር ብቻ መሆን አለበት

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_buy = types.InlineKeyboardButton("💳 አፕሊኬሽኑን ግዛ (Buy App)", callback_data='buy_app')
    btn_info = types.InlineKeyboardButton("ℹ️ ስለ አፑ መረጃ (Features)", callback_data='app_info')
    btn_support = types.InlineKeyboardButton("📞 እገዛ / አግኙኝ (Support)", callback_data='support')
    markup.add(btn_buy, btn_info, btn_support)
    
    welcome_text = (
        "ሰላም! እንኳን ወደ ኦፊሴላዊው የ Home Monitor አፕ ማከፋፈያ ቦት በደህና መጡ።\n\n"
        "ይህንን ዘመናዊ አፕሊኬሽን በመግዛት ቤትዎን በስልክዎ ሆነው ደህንነቱ በተጠበቀ ሁኔታ ይቆጣጠሩ!"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'buy_app':
        text = (
            "💳 የክፍያ ዝርዝር (Payment Details)\n\n"
            "አፕሊኬሽኑን ለመግዛት የሚከተሉትን አካውንቶች ይጠቀሙ:\n"
            "• የንግድ ባንክ (CBE): 100024494927\n"
            "• ቴሌብር (Telebirr): +251913441125\n\n"
            "💰 ዋጋ: xxxx.xxx ብር\n\n"
            "ክፍያውን ከፈጸሙ በኋላ የክፍያውን ደረሰኝ (Screenshot) በዚህ ቦት ላይ ፎቶውን ይላኩልን!"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 ወደ ዋናው ምናሌ ይመለሱ", callback_data='back_home'))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        
    elif call.data == 'app_info':
        text = (
            "ℹ️ የአፕሊኬሽኑ ዋና ዋና ባህሪያት:\n\n"
            "• የካሜራ ክትትል (Live Camera Streaming)\n"
            "• የርቀት ማስተካከያ እና ማንቂያ (Remote Alerts)\n"
            "• ደህንነቱ የተጠበቀ የምስጠራ ስርዓት (Secure Encryption)\n"
            "• ፈጣን የቪዲዮ ታሪክ አስተዳደር"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 ወደ ዋናው ምናሌ ይመለሱ", callback_data='back_home'))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        
    elif call.data == 'support':
        text = (
            "📞 የእገዛ ማዕከል (Customer Support)\n\n"
            "ለማንኛውም ጥያቄ ወይም እርዳታ በሚከተሉት አድራሻዎች ያግኙን:\n"
            "• ስልክ ቁጥር: +251913441125\n"
            "• ኢሜይል: ma.abdela@gmail.com"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 ወደ ዋናው ምናሌ ይመለሱ", callback_data='back_home'))
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup)
        
    elif call.data == 'back_home':
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_buy = types.InlineKeyboardButton("💳 አፕሊኬሽኑን ግዛ (Buy App)", callback_data='buy_app')
        btn_info = types.InlineKeyboardButton("ℹ️ ስለ አፑ መረጃ (Features)", callback_data='app_info')
        btn_support = types.InlineKeyboardButton("📞 እገዛ / አግኙኝ (Support)", callback_data='support')
        markup.add(btn_buy, btn_info, btn_support)
        
        welcome_text = (
            "ሰላም! እንኳን ወደ ኦፊሴላዊው የ Home Monitor አፕ ማከፋፈያ ቦት በደህና መጡ።\n\n"
            "ይህንን ዘመናዊ አፕሊኬሽን በመግዛት ቤትዎን በስልክዎ ሆነው ደህንነቱ በተጠበቀ ሁኔታ ይቆጣጠሩ!"
        )
        bot.edit_message_text(welcome_text, call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.message_handler(content_types=['photo'])
def handle_receipt(message):
    user = message.from_user
    caption = (
        "አዲስ ክፍያ ገብቷል!\n\n"
        f"ስም: {user.first_name}\n"
        f"ዩዘርናም: @{user.username if user.username else 'N/A'}\n"
        f"ዩዘር ID: {user.id}\n\n"
        "እዲስ ክፍያ ገብቶል ለማረጋገጥ ይህንን ኮፒ አድርገህ ኮዱን ሞልተህ ላክ፡\n"
        f"/approve {user.id} [Activation_Code_እዚህ_አስገባ]\n\n"
        "ወይም ደረሰኙ ትክክለኛ ካልሆነ:\n"
        f"/reject {user.id}"
    )
    
    markup = types.InlineKeyboardMarkup()
    btn_approve = types.InlineKeyboardButton("✅ አጽድቅ (Approve)", callback_data=f"approve_{user.id}")
    btn_reject = types.InlineKeyboardButton("❌ ውድቅ አድርግ (Reject)", callback_data=f"reject_{user.id}")
    markup.add(btn_approve, btn_reject)
    
    bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=caption)
    bot.reply_to(message, "✅ የክፍያ ደረሰኝዎ ደርሷል! አድሚኑ እስኪያረጋግጠው እባክዎ በትዕግስት ይጠብቁ።")

@bot.message_handler(commands=['approve'])
def cmd_approve(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "ይህንን ትዕዛዝ ለመፈጸም ፈቃድ የለዎትም!")
        return
        
    parts = message.text.split(maxsplit=2)
    if len(parts) < 2:
        bot.reply_to(message, "እባክዎ ትክክለኛውን ትዕዛዝ ያስገቡ።\nአጠቃቀም: /approve <user_id> <activation_code>")
        return
        
    try:
        target_user_id = int(parts[1])
        activation_code = parts[2] if len(parts) > 2 else "KEY-DEFAULT"
    except ValueError:
        bot.reply_to(message, "ትክክለኛ የዩዘር ID አልሰጡም።")
        return
        
    user_msg = (
        "🎉 ክፍያዎ በአድሚኑ ተረጋግጧል!\n\n"
        f"🔑 የአክቲቬሽን ኮድዎ: {activation_code}\n\n"
        "📥 አፑን ለማውረድ እና የ HOME MONITOR STORE ቻናሉን ለመቀላቀል ይህን ሊንክ ይጫኑ: https://t.me/+jcqrnUjZZLc2MmY8"
    )
    
    try:
        bot.send_message(target_user_id, user_msg)
        
        if os.path.exists('homemonitor.apk'):
            with open('homemonitor.apk', 'rb') as apk_file:
                bot.send_document(target_user_id, apk_file)
                
        bot.reply_to(message, f"✅ ለዩዘር ID {target_user_id} ክፍያው ጸድቆ ኮዱ እና የቻናሉ ሊንክ ተልኳል!")
    except Exception as e:
        bot.reply_to(message, f"⚠️ ስህተት ተፈጥሯል: {e}")

@bot.message_handler(commands=['reject'])
def cmd_reject(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "ይህንን ትዕዛዝ ለመፈጸም ፈቃድ የለዎትም!")
        return
        
    parts = message.text.split()
    if len(parts) < 2:
        bot.reply_to(message, "እባክዎ የዩዘር ID ያስገቡ።\nአጠቃቀም: /reject <user_id>")
        return
        
    try:
        target_user_id = int(parts[1])
    except ValueError:
        bot.reply_to(message, "ትክክለኛ የዩዘር ID አልሰጡም።")
        return
        
    bot.send_message(target_user_id, "❌ ይቅርታ፣ የላኩት የክፍያ ደረሰኝ ትክክለኛ አይደለም። እባክዎ ትክክለኛውን ደረሰኝ በድጋሚ ይላኩ።")
    bot.reply_to(message, f"❌ ለዩዘር ID {target_user_id} ክፍያው ውድቅ ተደርጓል (ደረሰኙ ትክክለኛ አይደለም)!")

@bot.callback_query_handler(func=lambda call: call.data.startswith('approve_') or call.data.startswith('reject_'))
def admin_action(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "ይህንን ትዕዛዝ ለመፈጸም ፈቃድ የለዎትም!", show_alert=True)
        return
        
    action, target_user_id = call.data.split('_')
    target_user_id = int(target_user_id)
    
    if action == 'approve':
        user_msg = (
            "🎉 ክፍያዎ በአድሚኑ ተረጋግጧል!\n\n"
            "🔑 የአክቲቬሽን ኮድዎ: HM-PRO-2026\n\n"
            "📥 አፑን ለማውረድ እና የ HOME MONITOR STORE ቻናሉን ለመቀላቀል ይህን ሊንክ ይጫኑ: https://t.me/+jcqrnUjZZLc2MmY8"
        )
        bot.send_message(target_user_id, user_msg)
        try:
            if os.path.exists('homemonitor.apk'):
                with open('homemonitor.apk', 'rb') as apk_file:
                    bot.send_document(target_user_id, apk_file)
        except Exception:
            pass
            
        bot.edit_message_caption("✅ ክፍያው ጸድቆ አፑ እና የቻናሉ ሊንክ ለተጠቃሚው ተልኳል!", call.message.chat.id, call.message.message_id)
    else:
        bot.send_message(target_user_id, "❌ ይቅርታ፣ የላኩት የክፍያ ደረሰኝ ትክክለኛ አይደለም። እባክዎ ትክክለኛውን ደረሰኝ በድጋሚ ይላኩ።")
        bot.edit_message_caption("❌ ክፍያው ውድቅ ተደርጓል (ደረሰኙ ትክክለኛ አይደለም)!", call.message.chat.id, call.message.message_id)

if __name__ == '__main__':
    print("Bot is running successfully...")
    bot.infinity_polling()