import logging
import os
import faq_data
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler,
    filters, ContextTypes, PicklePersistence,
)
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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# مجلد الملفات المسموح بإرسالها فقط (يمنع الوصول لأي ملف آخر على السيرفر)
FILES_DIR = os.path.join(BASE_DIR, "files")

# ملف حفظ تفضيلات المستخدمين (مثل اللغة المختارة) حتى تضل محفوظة بعد إعادة تشغيل البوت
PERSISTENCE_FILE = os.path.join(BASE_DIR, "bot_persistence.pickle")

# رقم التواصل مع الدعم (يفتح واتساب مباشرة، بدون إظهار الرقم للمستخدم)
SUPPORT_PHONE = "+963933339739"

# =========================================================
# نصوص الواجهة الثابتة بلغتين (عربي / إنكليزي)
# =========================================================
LANG_AR_BTN = "🇸🇾 العربية"
LANG_EN_BTN = "🇬🇧 English"

CHOOSE_LANG_TEXT = "🌐 الرجاء اختيار اللغة / Please choose your language:"

WELCOME_TEXT = {
    "ar": "أهلاً بك في شركة الشمعة للملكية الفكرية. كيف يمكننا مساعدتكم ؟",
    "en": "Welcome to Chamaa Intellectual Property Company. How can we help you ?",
}

START_BTN = {"ar": "🚀 ابدأ الخدمة", "en": "🚀 Start"}
CONTACT_BTN = {"ar": "📞 تواصل معنا", "en": "📞 Contact Us"}
BACK_BTN = {"ar": "🔙 رجوع", "en": "🔙 Back"}
HOME_BTN = {"ar": "🏠 القائمة الرئيسية", "en": "🏠 Main Menu"}
NO_TEXT = {"ar": "لا يوجد نص", "en": "No text available"}
FILE_NOT_FOUND = {"ar": "عذراً، الملف غير موجود حالياً.", "en": "Sorry, the file is currently unavailable."}
FILE_SEND_ERROR = {"ar": "عذراً، حصل خطأ أثناء إرسال الملف.", "en": "Sorry, an error occurred while sending the file."}

COMPANY_CONTACT_TEXT = {
    "ar": (
        "📞 *تواصل معنا عبر الأرقام التالية:*\n\n"
        "📱 011-2323014\n📱 011-2323036\n📱 011-4434085\n📱 011-4434086\n\n"
        "📧 *البريد الإلكتروني:*\n📩 info@chamaa.com"
    ),
    "en": (
        "📞 *Contact us via the following numbers:*\n\n"
        "📱 011-2323014\n📱 011-2323036\n📱 011-4434085\n📱 011-4434086\n\n"
        "📧 *Email:*\n📩 info@chamaa.com"
    ),
}

SUPPORT_NOTE = {
    "ar": "\n\n💬 *للرد السريع، تواصل مع فريق الدعم مباشرة عبر واتساب من الزر أدناه 👇*",
    "en": "\n\n💬 *For a quick reply, contact our support team directly via WhatsApp using the button below 👇*",
}

SUPPORT_BTN_TEXT = {
    "ar": "👈 اضغط هنا للتواصل الفوري مع الدعم 💬",
    "en": "👈 Tap here to contact support instantly 💬",
}


# دالة مساعدة لتحويل رقم الهاتف إلى رابط محادثة واتساب صالح
# (تحول الرقم المحلي مثل 0983918824 إلى https://wa.me/963983918824)
def make_whatsapp_link(phone: str) -> str:
    digits = "".join(ch for ch in phone if ch.isdigit())
    if digits.startswith("00"):
        digits = digits[2:]
    elif digits.startswith("0"):
        digits = "963" + digits[1:]
    return f"https://wa.me/{digits}"


def get_lang(context: ContextTypes.DEFAULT_TYPE) -> str:
    """يرجع لغة المستخدم المختارة، أو 'ar' افتراضياً إذا ما اختار بعد."""
    return context.user_data.get("lang", "ar")


def t(field, lang):
    """يرجع القيمة المناسبة من حقل ثنائي اللغة {'ar':.., 'en':..}، مع رجوع آمن لو الحقل نص عادي."""
    if isinstance(field, dict):
        return field.get(lang, field.get("ar", ""))
    return field


def main_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [[START_BTN[lang]], [CONTACT_BTN[lang]], [LANG_AR_BTN, LANG_EN_BTN]],
        resize_keyboard=True,
    )


def language_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup([[LANG_AR_BTN, LANG_EN_BTN]], resize_keyboard=True)


# دالة مساعدة لجلب العقدة
def get_node(path):
    try:
        node = faq_data.TREE["root"]
        if path == "root":
            return node
        for key in path.split("/"):
            node = node["children"][key]
        return node
    except KeyError:
        return None


# دالة بناء القائمة (معدلة لتكون أكثر أماناً + دعم اللغتين)
def build_inline_menu(path, lang):
    node = get_node(path)
    if not node:
        return None

    buttons = []
    children = node.get("children", {})

    # إضافة الأزرار للأبناء
    for key, child in children.items():
        new_path = f"{path}/{key}" if path != "root" else key
        callback = f"path:{new_path}"
        if child.get("redirect"):
            callback = f"path:{child['redirect']}"
        elif child.get("file"):
            callback = f"file:{child['file']}"
        buttons.append([InlineKeyboardButton(t(child["title"], lang), callback_data=callback)])

    # جهات الاتصال الخاصة بالعقدة
    if "contacts" in node:
        for c in node["contacts"]:
            phone = c.get("phone")
            if phone:
                buttons.append([InlineKeyboardButton(f"💬 {t(c['name'], lang)}", url=make_whatsapp_link(phone))])

    # أزرار التنقل
    if path != "root":
        buttons.append([InlineKeyboardButton(
            BACK_BTN[lang],
            callback_data=f"path:{path.rsplit('/', 1)[0] if '/' in path else 'root'}"
        )])
        buttons.append([InlineKeyboardButton(HOME_BTN[lang], callback_data="path:root")])

    return InlineKeyboardMarkup(buttons)


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "lang" in context.user_data:
        lang = context.user_data["lang"]
        await update.message.reply_text(WELCOME_TEXT[lang], reply_markup=main_keyboard(lang))
    else:
        await update.message.reply_text(CHOOSE_LANG_TEXT, reply_markup=language_keyboard())


async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # اختيار اللغة (متاح دائماً بغض النظر عن الحالة الحالية)
    if text == LANG_AR_BTN:
        context.user_data["lang"] = "ar"
        await update.message.reply_text(WELCOME_TEXT["ar"], reply_markup=main_keyboard("ar"))
        return
    if text == LANG_EN_BTN:
        context.user_data["lang"] = "en"
        await update.message.reply_text(WELCOME_TEXT["en"], reply_markup=main_keyboard("en"))
        return

    lang = get_lang(context)

    if text == START_BTN[lang]:
        node = get_node("root")
        await update.message.reply_text(t(node["text"], lang), reply_markup=build_inline_menu("root", lang))
        return

    if text == CONTACT_BTN[lang]:
        support_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(SUPPORT_BTN_TEXT[lang], url=make_whatsapp_link(SUPPORT_PHONE))]
        ])
        contact_text = COMPANY_CONTACT_TEXT[lang] + SUPPORT_NOTE[lang]
        await update.message.reply_text(contact_text, parse_mode="Markdown", reply_markup=support_keyboard)
        return


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    lang = get_lang(context)

    if data.startswith("path:"):
        path = data.split(":", 1)[1]
        node = get_node(path)
        if node:
            # نستخدم reply_text بدل edit_text حتى يرسل البوت رسالة جديدة بالأسفل بدل مسح القديمة
            await query.message.reply_text(
                t(node.get("text", NO_TEXT), lang),
                reply_markup=build_inline_menu(path, lang)
            )

    elif data.startswith("file:"):
        # نأخذ اسم الملف فقط (بدون أي مسار) لمنع الهروب خارج مجلد الملفات
        requested_name = os.path.basename(data.split(":", 1)[1])
        file_path = os.path.join(FILES_DIR, requested_name)

        # تأكيد إضافي: الملف الناتج لازم يكون فعلياً داخل FILES_DIR
        if not os.path.abspath(file_path).startswith(os.path.abspath(FILES_DIR) + os.sep):
            logging.warning(f"محاولة وصول مشبوهة لملف خارج المجلد المسموح: {requested_name}")
            await query.message.reply_text(FILE_NOT_FOUND[lang])
            return

        if not os.path.isfile(file_path):
            await query.message.reply_text(FILE_NOT_FOUND[lang])
            return

        try:
            with open(file_path, "rb") as f:
                await context.bot.send_document(chat_id=query.message.chat_id, document=f)
        except Exception as e:
            logging.error(f"خطأ أثناء إرسال الملف {requested_name}: {e}")
            await query.message.reply_text(FILE_SEND_ERROR[lang])


def main():
    persistence = PicklePersistence(filepath=PERSISTENCE_FILE)
    app = Application.builder().token(BOT_TOKEN).persistence(persistence).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(MessageHandler(filters.TEXT, text_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("البوت يعمل الآن...")
    app.run_polling()


if __name__ == "__main__":
    main()