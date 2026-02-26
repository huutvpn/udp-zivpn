
import json
import subprocess
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

CONFIG_FILE = "bot_config.json"

def load_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)

config = load_config()
TOKEN = config["TOKEN"]
ADMIN_ID = config["ADMIN_ID"]

user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Create"], ["Delete"], ["Check"]]
    await update.message.reply_text(
        "Menu Bot ZIVPN",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    if text == "Create":
        user_state[user_id] = {"step": "username"}
        await update.message.reply_text("Masukkan username:")
        return

    if user_id in user_state:
        state = user_state[user_id]

        if state["step"] == "username":
            state["username"] = text
            state["step"] = "password"
            await update.message.reply_text("Masukkan password:")
            return

        if state["step"] == "password":
            state["password"] = text
            state["step"] = "duration"
            await update.message.reply_text("Durasi (hari):")
            return

        if state["step"] == "duration":
            state["duration"] = text
            state["step"] = "limit"
            await update.message.reply_text("Limit IP:")
            return

        if state["step"] == "limit":
            state["limit"] = text

            try:
                subprocess.run([
                    "bash", "zi.sh",
                    state["username"],
                    state["password"],
                    state["duration"],
                    state["limit"]
                ])
                await update.message.reply_text("Akun berhasil dibuat di server")
            except Exception as e:
                await update.message.reply_text(f"ERROR: {e}")

            del user_state[user_id]
            return

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
