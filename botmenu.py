
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import subprocess

TOKEN = "ISI_TOKEN_KAMU"
ADMINS = [6479897007]  # tambah ID admin di sini

MENU_CMD = "/usr/local/bin/zivpn-menu.sh"

def is_admin(user_id):
    return user_id in ADMINS

def run_cmd(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, timeout=15)
        return output.decode("utf-8")[:4000]
    except Exception as e:
        return str(e)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("Unauthorized")
        return

    buttons = [
        [InlineKeyboardButton("➕ Add Regular", callback_data='1'),
         InlineKeyboardButton("🎁 Add Trial", callback_data='2')],
        [InlineKeyboardButton("📋 List Akun", callback_data='3'),
         InlineKeyboardButton("❌ Delete Akun", callback_data='4')],
        [InlineKeyboardButton("⏳ Edit Expiry", callback_data='5'),
         InlineKeyboardButton("🔑 Edit Password", callback_data='6')],
        [InlineKeyboardButton("🖥 VPS Info", callback_data='7'),
         InlineKeyboardButton("💾 Backup/Restore", callback_data='8')],
        [InlineKeyboardButton("🤖 Bot Settings", callback_data='9'),
         InlineKeyboardButton("🎨 Theme", callback_data='10')],
        [InlineKeyboardButton("🌐 Edit Domain", callback_data='11'),
         InlineKeyboardButton("♻ Update Script", callback_data='16')],
        [InlineKeyboardButton("📊 Cek CPU/RAM", callback_data='15')],
    ]

    await update.message.reply_text(
        "ZIVPN BOT MENU",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not is_admin(query.from_user.id):
        await query.edit_message_text("Unauthorized")
        return

    choice = query.data
    cmd = f'echo "{choice}" | {MENU_CMD}'
    result = run_cmd(cmd)

    await query.edit_message_text(f"Output:\n{result}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))

app.run_polling()
