import telebot
import json
import subprocess
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *

bot = telebot.TeleBot(BOT_TOKEN)
DB_FILE = "users.json"

SERVERS = {
    "SG-1": 10000,
    "SG-2": 20000
}

def load_db():
    try:
        with open(DB_FILE) as f:
            return json.load(f)
    except:
        return {}

def save_db(db):
    with open(DB_FILE, "w") as f:
        json.dump(db, f, indent=2)

def main_menu():
    m = InlineKeyboardMarkup()
    m.add(InlineKeyboardButton("➕ Buat Akun", callback_data="buat"))
    m.add(InlineKeyboardButton("💰 Saldo", callback_data="saldo"))
    m.add(InlineKeyboardButton("💳 TopUp", callback_data="topup"))
    return m

def server_menu():
    m = InlineKeyboardMarkup()
    for s, harga in SERVERS.items():
        m.add(InlineKeyboardButton(f"{s} - Rp {harga}", callback_data=f"server|{s}"))
    return m

@bot.message_handler(commands=['start'])
def start(msg):
    db = load_db()
    uid = str(msg.from_user.id)

    if uid not in db:
        db[uid] = {"saldo": 0, "role": "user"}
        save_db(db)

    bot.send_message(msg.chat.id, "Menu Bot", reply_markup=main_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    db = load_db()
    uid = str(call.from_user.id)

    if call.data == "saldo":
        saldo = "∞ (Unlimited)" if uid == ADMIN_ID else db[uid]["saldo"]
        bot.answer_callback_query(call.id, f"Saldo: {saldo}")

    elif call.data == "topup":
        bot.send_message(call.message.chat.id, "Silakan bayar QRIS:")
        bot.send_photo(call.message.chat.id, open("qris.jpg", "rb"))

    elif call.data == "buat":
        bot.send_message(call.message.chat.id, "Pilih Server:", reply_markup=server_menu())

    elif call.data.startswith("server"):
        server = call.data.split("|")[1]
        bot.send_message(call.message.chat.id, f"Format: user pass durasi limit_ip\nServer: {server}")
        bot.register_next_step_handler(call.message, lambda m: process_create(m, server))

def process_create(msg, server):
    db = load_db()
    uid = str(msg.from_user.id)

    try:
        user, pwd, dur, limit_ip = msg.text.split()
    except:
        return bot.send_message(msg.chat.id, "Format salah")

    harga = SERVERS[server]

    # Reseller discount
    if db.get(uid, {}).get("role") == "reseller":
        harga = int(harga * RESELLER_DISCOUNT)

    # ADMIN BYPASS
    if uid != ADMIN_ID:
        if db[uid]["saldo"] < harga:
            return bot.send_message(msg.chat.id, "Saldo tidak cukup")

        db[uid]["saldo"] -= harga
        save_db(db)

    cmd = f"addzivpn {user} {pwd} {dur} {limit_ip}"
    hasil = subprocess.getoutput(cmd)

    bot.send_message(msg.chat.id, f"✅ Akun dibuat di {server}\n{hasil}")

print("Bot aktif...")
bot.infinity_polling()
