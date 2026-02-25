
import json
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

CONFIG_FILE = "bot_config.json"

def load_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)

def load_users(db_path):
    try:
        with open(db_path) as f:
            return json.load(f)
    except:
        return []

def save_users(db_path, data):
    with open(db_path, "w") as f:
        json.dump(data, f, indent=2)

config = load_config()
USER_DB = config["USER_DB"]

user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("➕ Create Account", callback_data="create")],
        [InlineKeyboardButton("❌ Delete Account", callback_data="delete")],
        [InlineKeyboardButton("👤 Check Account", callback_data="check")],
        [InlineKeyboardButton("📋 List Accounts", callback_data="list")]
    ]
    await update.message.reply_text("Menu Bot ZIVPN", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    chat_id = query.message.chat_id

    if query.data == "create":
        user_state[chat_id] = {"step": "username"}
        await query.message.reply_text("Masukkan username:")

    elif query.data == "delete":
        users = load_users(USER_DB)
        keyboard = [[InlineKeyboardButton(u["username"], callback_data=f"del_{u['username']}")] for u in users]
        await query.message.reply_text("Pilih user:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith("del_"):
        username = query.data.replace("del_", "")
        users = load_users(USER_DB)
        users = [u for u in users if u["username"] != username]
        save_users(USER_DB, users)
        await query.message.reply_text(f"User {username} dihapus.")

    elif query.data == "list":
        users = load_users(USER_DB)
        text = "\\n".join([f"{u['username']} | IP Limit: {u.get('ip_limit', 1)}" for u in users]) or "Tidak ada akun."
        await query.message.reply_text(text)

    elif query.data == "check":
        users = load_users(USER_DB)
        keyboard = [[InlineKeyboardButton(u["username"], callback_data=f"chk_{u['username']}")] for u in users]
        await query.message.reply_text("Pilih user:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith("chk_"):
        username = query.data.replace("chk_", "")
        users = load_users(USER_DB)
        user = next((u for u in users if u["username"] == username), None)
        if not user:
            await query.message.reply_text("User tidak ditemukan.")
            return

        now = int(time.time())
        remaining = user["expiry_timestamp"] - now
        days = remaining // 86400
        text = (
            f"User: {user['username']}\\n"
            f"Limit IP: {user.get('ip_limit', 1)}\\n"
            f"Sisa: {days} hari"
        )
        await query.message.reply_text(text)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    if chat_id not in user_state:
        return

    state = user_state[chat_id]

    if state["step"] == "username":
        state["username"] = update.message.text
        state["step"] = "password"
        await update.message.reply_text("Masukkan password:")

    elif state["step"] == "password":
        state["password"] = update.message.text
        state["step"] = "duration"
        await update.message.reply_text("Durasi (hari):")

    elif state["step"] == "duration":
        state["duration"] = int(update.message.text)
        state["step"] = "limit"
        await update.message.reply_text("Limit IP:")

    elif state["step"] == "limit":
        state["limit"] = int(update.message.text)

        users = load_users(USER_DB)
        expiry = int(time.time()) + state["duration"] * 86400

        users.append({
            "username": state["username"],
            "password": state["password"],
            "expiry_timestamp": expiry,
            "ip_limit": state["limit"]
        })

        save_users(USER_DB, users)

        await update.message.reply_text("Akun berhasil dibuat.")
        del user_state[chat_id]

def main():
    app = ApplicationBuilder().token(load_config()["BOT_TOKEN"]).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
