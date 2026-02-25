
import telebot
import json
import subprocess
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *

bot = telebot.TeleBot(BOT_TOKEN)
DB_FILE = "users.json"

user_state = {}

def load_db():
    try:
        with open(DB_FILE) as f:
            return json.load(f)
    except:
        return {}

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

def menu():
    m = InlineKeyboardMarkup()
    m.add(
        InlineKeyboardButton("➕ Buat Akun", callback_data="buat"),
        InlineKeyboardButton("💰 Saldo", callback_data="saldo")
    )
    m.add(InlineKeyboardButton("💳 TopUp", callback_data="topup"))
    return m

@bot.message_handler(commands=['start'])
def start(msg):
    db = load_db()
    uid = str(msg.from_user.id)

    if uid not in db:
        db[uid] = {"saldo": 0}
        save_db(db)

    bot.send_message(msg.chat.id, "Menu Bot", reply_markup=menu())

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    db = load_db()
    uid = str(call.from_user.id)

    if call.data == "saldo":
        saldo = db.get(uid, {}).get("saldo", 0)
        bot.answer_callback_query(call.id, f"Saldo: Rp {saldo}")

    elif call.data == "topup":
        bot.send_message(call.message.chat.id, "Silakan bayar QRIS:")
        try:
            bot.send_photo(call.message.chat.id, open("qris.jpg", "rb"))
        except:
            bot.send_message(call.message.chat.id, "qris.jpg tidak ditemukan")

    elif call.data == "buat":
        user_state[uid] = {}
        bot.send_message(call.message.chat.id, "Masukkan Username:")
        bot.register_next_step_handler(call.message, step_user)

def step_user(msg):
    uid = str(msg.from_user.id)
    user_state.setdefault(uid, {})["user"] = msg.text
    bot.send_message(msg.chat.id, "Masukkan Password:")
    bot.register_next_step_handler(msg, step_pass)

def step_pass(msg):
    uid = str(msg.from_user.id)
    user_state.setdefault(uid, {})["pass"] = msg.text
    bot.send_message(msg.chat.id, "Masukkan Durasi (hari):")
    bot.register_next_step_handler(msg, step_dur)

def step_dur(msg):
    db = load_db()
    uid = str(msg.from_user.id)

    try:
        durasi = int(msg.text)
    except:
        return bot.send_message(msg.chat.id, "Durasi harus angka")

    data = user_state.get(uid)
    if not data:
        return bot.send_message(msg.chat.id, "Session expired")

    username = data["user"]
    password = data["pass"]

    harga = PRICE

    if uid != str(ADMIN_ID):
        saldo = db.get(uid, {}).get("saldo", 0)
        if saldo < harga:
            return bot.send_message(msg.chat.id, "Saldo tidak cukup")

        db[uid]["saldo"] -= harga
        save_db(db)

    hasil = subprocess.getoutput(f"addzivpn {username} {password} {durasi}")
    bot.send_message(msg.chat.id, hasil)

print("Bot aktif...")
bot.infinity_polling()
