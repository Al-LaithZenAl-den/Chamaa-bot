import logging
import importlib
import os

import faq_data
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# ============================= إعدادات البوت =============================
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("تحذير: لم يتم العثور على BOT_TOKEN في متغيرات النظام.")

logging.basicConfig(format="%(asctime)s | %(levelname)s | %(message)s", level=logging.INFO)

# أرقام التواصل العامة للشركة
COMPANY_CONTACT_TEXT = (
    "📞 *تواصل معنا عبر الأرقام التالية:*\n\n"
    "📱 [011-2323014](tel:0112323014)\n"
    "📱 [011-2323036](tel:0112323036)\n"
    "📱 [011-4434085](tel:0114434085)\n"
    "📱 [011-4434086](tel:0114434086)\n\n"
    "📧 *أو راسلنا عبر البريد الإلكتروني:*\n"
    "📩 [info@chamaa.com](mailto:info@chamaa.com)"
)


# ============================= أدوات مساعدة للشجرة =============================

def get_node(path):
    """إحضار العقدة المطابقة لمسار معين، مثال: 'trademarks/reg_syria/steps'."""
    node = faq_data.TREE["root"]
    if path == "root":
        return node
    for key in path.split("/"):
        node = node["children"][key]
    return node


def parent_of(path):
    """إرجاع (مسار الأب، مفتاح العقدة الحالية) أو (None, None) إذا كانت العقدة هي الجذر."""
    if path == "root":
        return None, None
    if "/" in path:
        parent_path, key = path.rsplit("/", 1)
        return parent_path, key
    return "root", path


def find_contacts(path):
    """البحث عن جهات التواصل بدءاً من العقدة الحالية وصعوداً حتى الجذر."""
    current_path = path
    while True:
        node = get_node(current_path)
        if node.get("contacts"):
            return node["contacts"]
        parent_path, _ = parent_of(current_path)
        if parent_path is None:
            return None
        current_path = parent_path


def build_node_text(node):
    text = node.get("text", "")
    if node.get("staff"):
        text += f"\n\n👤 المسؤول عن هذا القسم: {node['staff']}"
    return text


def build_inline_menu(path):
    node = get_node(path)
    mode = node.get("mode", "menu")
    children = node.get("children")
    buttons = []

    def child_button(key, child, base_path):
        new_path = f"{base_path}/{key}" if base_path != "root" else key
        if child.get("redirect"):
            return InlineKeyboardButton(child["title"], callback_data=f"path:{child['redirect']}")
        if child.get("file") and not child.get("children"):
            return InlineKeyboardButton(child["title"], callback_data=f"file:{child['file']}")
        return InlineKeyboardButton(child["title"], callback_data=f"path:{new_path}")

    if children and mode == "menu":
        # عرض كل الأبناء كخيارات للاختيار من بينها
        for key, child in children.items():
            buttons.append([child_button(key, child, path)])

    elif children and mode == "sequential":
        # عرض أول سؤال في التسلسل فقط
        first_key = next(iter(children))
        first_child = children[first_key]
        label = f"➡️ {first_child['title']}"
        target = child_button(first_key, first_child, path)
        buttons.append([InlineKeyboardButton(label, callback_data=target.callback_data)])

    else:
        # عقدة نهائية (leaf) - تحقق إن كان أبوها تسلسلياً ليتم عرض "السؤال التالي"
        parent_path, cur_key = parent_of(path)
        if parent_path is not None:
            parent = get_node(parent_path)
            if parent.get("mode") == "sequential" and parent.get("children"):
                keys = list(parent["children"].keys())
                idx = keys.index(cur_key)
                if idx + 1 < len(keys):
                    next_key = keys[idx + 1]
                    next_child = parent["children"][next_key]
                    label = f"➡️ {next_child['title']}"
                    target = child_button(next_key, next_child, parent_path)
                    buttons.append([InlineKeyboardButton(label, callback_data=target.callback_data)])

    # زر تحميل ملف مرفق بالعقدة نفسها (وليس عبر عقدة ابن منفصلة)
    if node.get("file") and not (children and mode == "menu"):
        buttons.append([InlineKeyboardButton("📥 تحميل الملف", callback_data=f"file:{node['file']}")])

    # جهات التواصل
    contacts = find_contacts(path)
    if contacts:
        for c in contacts:
            name = c["name"]
            phone = c.get("phone")
            if phone:
                buttons.append([InlineKeyboardButton(f"📞 {name} {phone}", url=f"tel:{phone}")])
            else:
                buttons.append([InlineKeyboardButton(f"📞 {name}", callback_data=f"dept:{name}")])

    if node.get("general_contact"):
        buttons.append([InlineKeyboardButton("📞 تواصل معنا", callback_data="general_contact")])

    # أزرار التنقل
    if path != "root":
        parent_path, _ = parent_of(path)
        buttons.append([InlineKeyboardButton("🔙 الرجوع للخلف", callback_data=f"path:{parent_path}")])
        buttons.append([InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="path:root")])

    return InlineKeyboardMarkup(buttons)


# ============================= القائمة الثابتة (Reply Keyboard) =============================

def get_main_reply_keyboard():
    return ReplyKeyboardMarkup([
        ["🚀 ابدأ الخدمة"],
        ["📞 تواصل معنا"]
    ], resize_keyboard=True)


# ============================= المعالجات (Handlers) =============================

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
        await update.message.reply_text(
            build_node_text(get_node("root")),
            reply_markup=build_inline_menu("root")
        )

    elif text == "📞 تواصل معنا":
        await update.message.reply_text(COMPANY_CONTACT_TEXT, parse_mode="Markdown")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    # إرسال ملف مرفق
    if data.startswith("file:"):
        file_name = data.split(":", 1)[1]
        try:
            await context.bot.send_document(chat_id=query.message.chat_id, document=open(file_name, "rb"))
            await query.answer("تم إرسال الملف!")
        except Exception as e:
            logging.error(f"خطأ في إرسال الملف: {e}")
            await query.answer("عذراً، حدث خطأ أثناء إرسال الملف.")
        return

    # زر "تواصل معنا" العام
    if data == "general_contact":
        await query.message.reply_text(COMPANY_CONTACT_TEXT, parse_mode="Markdown")
        return

    # زر جهة تواصل بدون رقم هاتف مباشر
    if data.startswith("dept:"):
        dept_name = data.split(":", 1)[1]
        await query.message.reply_text(
            f"للتواصل مع *{dept_name}*، يرجى استخدام أرقام الشركة العامة:\n\n{COMPANY_CONTACT_TEXT}",
            parse_mode="Markdown"
        )
        return

    # التنقل بين العقد
    try:
        importlib.reload(faq_data)
    except Exception as e:
        logging.error(f"فشل تحديث faq_data: {e}")

    if data.startswith("path:"):
        path = data.split(":", 1)[1]
        node = get_node(path)
        await query.message.reply_text(
            build_node_text(node),
            reply_markup=build_inline_menu(path)
        )


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()


if __name__ == "__main__":
    main()