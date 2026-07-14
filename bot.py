import logging
import importlib
import os
import faq_data
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# إعدادات البوت
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)

# أرقام التواصل العامة
COMPANY_CONTACT_TEXT = (
    "📞 *تواصل معنا عبر الأرقام التالية:*\n\n"
    "📱 011-2323014\n📱 011-2323036\n📱 011-4434085\n📱 011-4434086\n\n"
    "📧 *البريد الإلكتروني:*\n📩 info@chamaa.com"
)

# دالة مساعدة لتحويل رقم الهاتف إلى رابط محادثة واتساب صالح
# (تحول الرقم المحلي مثل 0983918824 إلى https://wa.me/963983918824)
def make_whatsapp_link(phone: str) -> str:
    digits = "".join(ch for ch in phone if ch.isdigit())
    if digits.startswith("00"):
        digits = digits[2:]
    elif digits.startswith("0"):
        digits = "963" + digits[1:]
    return f"https://wa.me/{digits}"

# دالة مساعدة لجلب العقدة
def get_node(path):
    try:
        node = faq_data.TREE["root"]
        if path == "root": return node
        for key in path.split("/"):
            node = node["children"][key]
        return node
    except KeyError:
        return None

# دالة بناء القائمة (معدلة لتكون أكثر أماناً)
def build_inline_menu(path):
    node = get_node(path)
    if not node: return None
    
    buttons = []
    children = node.get("children", {})

    # إضافة الأزرار للأبناء
    for key, child in children.items():
        new_path = f"{path}/{key}" if path != "root" else key
        callback = f"path:{new_path}"
        if child.get("redirect"): callback = f"path:{child['redirect']}"
        elif child.get("file"): callback = f"file:{child['file']}"
        buttons.append([InlineKeyboardButton(child["title"], callback_data=callback)])

    # جهات الاتصال الخاصة بالعقدة
    if "contacts" in node:
        for c in node["contacts"]:
            phone = c.get("phone")
            if phone:
                buttons.append([InlineKeyboardButton(f"💬 {c['name']}", url=make_whatsapp_link(phone))])

    # أزرار التنقل
    if path != "root":
        buttons.append([InlineKeyboardButton("🔙 رجوع", callback_data=f"path:{path.rsplit('/', 1)[0] if '/' in path else 'root'}")])
        buttons.append([InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="path:root")])

    return InlineKeyboardMarkup(buttons)

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = ReplyKeyboardMarkup([["🚀 ابدأ الخدمة"], ["📞 تواصل معنا"]], resize_keyboard=True)
    await update.message.reply_text("أهلاً بك في شركة الشمعة للملكية الفكرية. كيف يمكننا مساعدتك اليوم؟", reply_markup=keyboard)

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "🚀 ابدأ الخدمة":
        node = get_node("root")
        await update.message.reply_text(node["text"], reply_markup=build_inline_menu("root"))
    elif text == "📞 تواصل معنا":
        await update.message.reply_text(COMPANY_CONTACT_TEXT, parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("path:"):
        path = data.split(":", 1)[1]
        node = get_node(path)
        if node:
            # التعديل هنا: نستخدم reply_text بدل edit_text
            # هذا سيجعل البوت يرسل رسالة جديدة في الأسفل بدلاً من مسح القديمة
            await query.message.reply_text(
                node.get("text", "لا يوجد نص"), 
                reply_markup=build_inline_menu(path)
            )
    
    elif data.startswith("file:"):
        file_name = data.split(":", 1)[1]
        try:
            await context.bot.send_document(chat_id=query.message.chat_id, document=open(file_name, "rb"))
        except:
            await query.message.reply_text("عذراً، الملف غير موجود حالياً.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(MessageHandler(filters.TEXT, text_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()