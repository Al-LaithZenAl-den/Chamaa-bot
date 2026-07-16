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
if not BOT_TOKEN:
    raise RuntimeError(
        "لم يتم العثور على BOT_TOKEN. تأكد من إضافته كمتغير بيئة (Environment Variable) "
        "أو داخل ملف .env في نفس مجلد المشروع، ولا تكتبه مباشرة داخل الكود."
    )

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)

# أرقام التواصل العامة
COMPANY_CONTACT_TEXT = (
    "📞 *تواصل معنا عبر الأرقام التالية:*\n\n"
    "📱 011-2323014\n📱 011-2323036\n📱 011-4434085\n📱 011-4434086\n\n"
    "📧 *البريد الإلكتروني:*\n📩 info@chamaa.com"
)

# مجلد الملفات المسموح بإرسالها فقط (يمنع الوصول لأي ملف آخر على السيرفر)
FILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files")

# رقم التواصل مع الدعم (يفتح واتساب مباشرة، بدون إظهار الرقم للمستخدم)
SUPPORT_PHONE = "+963933339739"

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
        support_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("👈 اضغط هنا للتواصل الفوري مع الدعم 💬", url=make_whatsapp_link(SUPPORT_PHONE))]
        ])
        contact_text = COMPANY_CONTACT_TEXT + "\n\n💬 *للرد السريع، تواصل مع فريق الدعم مباشرة عبر واتساب من الزر أدناه 👇*"
        await update.message.reply_text(contact_text, parse_mode="Markdown", reply_markup=support_keyboard)

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
        # نأخذ اسم الملف فقط (بدون أي مسار) لمنع الهروب خارج مجلد الملفات
        requested_name = os.path.basename(data.split(":", 1)[1])
        file_path = os.path.join(FILES_DIR, requested_name)

        # تأكيد إضافي: الملف الناتج لازم يكون فعلياً داخل FILES_DIR
        if not os.path.abspath(file_path).startswith(os.path.abspath(FILES_DIR) + os.sep):
            logging.warning(f"محاولة وصول مشبوهة لملف خارج المجلد المسموح: {requested_name}")
            await query.message.reply_text("عذراً، الملف غير موجود حالياً.")
            return

        if not os.path.isfile(file_path):
            await query.message.reply_text("عذراً، الملف غير موجود حالياً.")
            return

        try:
            with open(file_path, "rb") as f:
                await context.bot.send_document(chat_id=query.message.chat_id, document=f)
        except Exception as e:
            logging.error(f"خطأ أثناء إرسال الملف {requested_name}: {e}")
            await query.message.reply_text("عذراً، حصل خطأ أثناء إرسال الملف.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(MessageHandler(filters.TEXT, text_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()