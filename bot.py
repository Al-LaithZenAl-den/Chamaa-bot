import logging
import faq_data
import importlib
import os # تأكد من استيراد os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# إعدادات البوت
# إعدادات البوت
load_dotenv()
# نحاول الحصول على التوكن من إعدادات النظام أولاً، ثم من ملف .env
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("تحذير: لم يتم العثور على BOT_TOKEN في متغيرات النظام.")

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)

# القائمة الرئيسية الثابتة
def get_main_reply_keyboard():
    return ReplyKeyboardMarkup([
        ["🚀 ابدأ الخدمة"],
        ["📞 تواصل معنا"]
    ], resize_keyboard=True)

# بناء القوائم الشجرية
def build_inline_menu(node, path):
    buttons = []
    if "children" in node:
        for key, child in node["children"].items():
            new_path = f"{path}/{key}" if path != "root" else key
            
            if "url" in child and child["url"].startswith("http"):
                buttons.append([InlineKeyboardButton(child["title"], url=child["url"])])
            # إضافة زر تحميل الملف إذا وجد في البيانات
            elif "file" in child:
                buttons.append([InlineKeyboardButton(child["title"], callback_data=f"file:{child['file']}")])
            else:
                buttons.append([InlineKeyboardButton(child["title"], callback_data=f"info:{new_path}")])
    
    if path != "root":
        buttons.append([InlineKeyboardButton("🔙 العودة للخلف", callback_data=f"path:{path.rsplit('/', 1)[0] if '/' in path else 'root'}")])
    
    return InlineKeyboardMarkup(buttons)

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "مرحباً بك في شركة الشمعة. استخدم الأزرار للبدء:",
        reply_markup=get_main_reply_keyboard()
    )

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        importlib.reload(faq_data)
    except Exception as e:
        logging.error(f"فشل تحديث faq_data: {e}")
    text = update.message.text
    if text == "🚀 ابدأ الخدمة":
        node = faq_data.TREE["root"]
        await update.message.reply_text(node["text"], reply_markup=build_inline_menu(node, "root"))
    
    elif text == "📞 تواصل معنا":
        await update.message.reply_text(
            "📞 *تواصل معنا عبر الأرقام التالية:*\n\n"
            "📱 [011-2323014](tel:0112323014)\n"
            "📱 [011-2323036](tel:0112323036)\n"
            "📱 [011-4434085](tel:0114434085)\n"
            "📱 [011-4434086](tel:0114434086)\n\n"
            "📧 *أو راسلنا عبر البريد الإلكتروني:*\n"
            "📩 [info@chamaa.com](mailto:info@chamaa.com)",
            parse_mode="Markdown"
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # معالجة تحميل الملف
    # معالجة تحميل الملف
    if query.data.startswith("file:"):
        file_name = query.data.split(":")[1]
        try:
            # نرسل الملف للمستخدم
            await context.bot.send_document(chat_id=query.message.chat_id, document=open(file_name, 'rb'))
            await query.answer("تم إرسال الملف!") # إشعار للمستخدم
        except Exception as e:
            logging.error(f"خطأ في إرسال الملف: {e}")
            await query.answer("عذراً، حدث خطأ أثناء إرسال الملف.")
        return

    # معالجة التنقل
    try:
        importlib.reload(faq_data)
    except Exception as e:
        logging.error(f"فشل تحديث faq_data: {e}")
    
    # منطق التنقل بين القوائم
    data_parts = query.data.split(":")
    action = data_parts[0]
    path = data_parts[1]
    
    node = faq_data.TREE["root"]
    if path != "root":
        for key in path.split("/"):
            node = node["children"][key]
            
    await query.message.reply_text(
        node["text"], 
        reply_markup=build_inline_menu(node, path)
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()