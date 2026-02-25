
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import subprocess

TOKEN = "ISI_TOKEN_KAMU"
ADMINS = [6479897007]

ENGINE = "zi.sh"

def is_admin(user_id):
    return user_id in ADMINS

def run_menu(choice):
    try:
        cmd = f'echo "{choice}" | {ENGINE}'
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=20)
        return output.decode("utf-8")[:4000]
    except Exception as e:
        return str(e)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("Unauthorized")
        return

    keyboard = [
        [InlineKeyboardButton("➕ Buat Akun", callback_data="1"),
         InlineKeyboardButton("🎁 Trial Akun", callback_data="2")],
        [InlineKeyboardButton("📋 List Akun", callback_data="3"),
         InlineKeyboardButton("❌ Hapus Akun", callback_data="4")],
        [InlineKeyboardButton("⏳ Perpanjang", callback_data="5"),
         InlineKeyboardButton("🔑 Ganti Password", callback_data="6")],
        [InlineKeyboardButton("🖥 Info Server", callback_data="7"),
         InlineKeyboardButton("💾 Backup", callback_data="8")],
        [InlineKeyboardButton("🌐 Edit Domain", callback_data="11"),
         InlineKeyboardButton("♻ Update", callback_data="16")],
        [InlineKeyboardButton("📊 CPU / RAM", callback_data="15")]
    ]

    await update.message.reply_text(
        "ZIVPN CONTROL PANEL",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not is_admin(query.from_user.id):
        await query.edit_message_text("Unauthorized")
        return

    result = run_menu(query.data)

    await query.edit_message_text(f"Output:\n{result}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(buttons))

app.run_polling()
