import logging
import faq_data
import importlib
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# إعدادات البيئة
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# التحقق من التوكن (بدون إيقاف البوت)
if not BOT_TOKEN:
    print("خطأ فادح: لم يتم العثور على BOT_TOKEN. تأكد من إضافته في إعدادات Railway")

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)

# القائمة الرئيسية
def get_main_reply_keyboard():
    return ReplyKeyboardMarkup([
        ["🚀 ابدأ الخدمة"],
        ["📞 تواصل معنا"]
    ], resize_keyboard=True)

# بناء القوائم
def build_inline_menu(node, path):
    buttons = []
    if "children" in node:
        for key, child in node["children"].items():
            new_path = f"{path}/{key}" if path != "root" else key
            if "url" in child and child["url"].startswith("http"):
                buttons.append([InlineKeyboardButton(child["title"], url=child["url"])])
            elif "file" in child:
                buttons.append([InlineKeyboardButton(child["title"], callback_data=f"file:{child['file']}")])
            else:
                buttons.append([InlineKeyboardButton(child["title"], callback_data=f"info:{new_path}")])
    
    if path != "root":
        buttons.append([InlineKeyboardButton("🔙 العودة للخلف", callback_data=f"path:{path.rsplit('/', 1)[0] if '/' in path else 'root'}")])
    
    return InlineKeyboardMarkup(buttons)

# معالجات الأوامر
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً بك في شركة الشمعة. استخدم الأزرار للبدء:", reply_markup=get_main_reply_keyboard())

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        importlib.reload(faq_data)
    except: pass
    
    text = update.message.text
    if text == "🚀 ابدأ الخدمة":
        node = faq_data.TREE["root"]
        await update.message.reply_text(node["text"], reply_markup=build_inline_menu(node, "root"))
    elif text == "📞 تواصل معنا":
        await update.message.reply_text("📞 تواصل معنا عبر الأرقام الموضحة في ملف البيانات الخاص بك.", parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("file:"):
        file_name = query.data.split(":")[1]
        try:
            await context.bot.send_document(chat_id=query.message.chat_id, document=open(file_name, 'rb'))
        except Exception as e:
            await query.answer("عذراً، حدث خطأ أثناء إرسال الملف.")
        return

    try:
        importlib.reload(faq_data)
    except: pass
    
    data_parts = query.data.split(":")
    path = data_parts[1]
    node = faq_data.TREE["root"]
    if path != "root":
        for key in path.split("/"):
            node = node["children"].get(key, node)
            
    await query.message.reply_text(node["text"], reply_markup=build_inline_menu(node, path))

def main():
    if not BOT_TOKEN: return
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()