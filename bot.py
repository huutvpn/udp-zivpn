import telebot
import json
import subprocess
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *

bot = telebot.TeleBot(BOT_TOKEN)
DB_FILE = "users.json"
pending_topup = {}

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
        bot.answer_callback_query(call.id, f"Saldo: Rp {db[uid]['saldo']}")

    elif call.data == "topup":
        bot.send_message(call.message.chat.id, "Silakan bayar QRIS lalu kirim bukti:")
        bot.send_photo(call.message.chat.id, open("qris.jpg", "rb"))

    elif call.data == "buat":
        bot.send_message(call.message.chat.id, "Format: user pass durasi")
        bot.register_next_step_handler(call.message, process_create)

@bot.message_handler(content_types=['photo'])
def handle_bukti(msg):
    uid = str(msg.from_user.id)

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("✅ Approve", callback_data=f"approve|{uid}"))

    bot.send_photo(
        ADMIN_ID,
        msg.photo[-1].file_id,
        caption=f"User {uid} kirim bukti topup",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("approve"))
def approve(call):
    uid = call.data.split("|")[1]
    pending_topup[call.message.chat.id] = uid

    bot.send_message(call.message.chat.id, "Masukkan nominal saldo:")
    bot.register_next_step_handler(call.message, isi_saldo)

def isi_saldo(msg):
    db = load_db()
    admin_chat = msg.chat.id
    target_uid = pending_topup.get(admin_chat)

    try:
        nominal = int(msg.text)
    except:
        return bot.send_message(admin_chat, "Nominal salah")

    if target_uid not in db:
        db[target_uid] = {"saldo": 0}

    db[target_uid]["saldo"] += nominal
    save_db(db)

    bot.send_message(admin_chat, f"Saldo user {target_uid} +{nominal}")
    bot.send_message(int(target_uid), f"✅ TopUp berhasil\nSaldo: Rp {db[target_uid]['saldo']}")

def process_create(msg):
    db = load_db()
    uid = str(msg.from_user.id)

    try:
        user, pwd, dur = msg.text.split()
    except:
        return bot.send_message(msg.chat.id, "Format salah")

    harga = PRICE

    # ADMIN BYPASS SALDO
    if uid != ADMIN_ID:
        if db[uid]["saldo"] < harga:
            return bot.send_message(msg.chat.id, "Saldo tidak cukup")

        db[uid]["saldo"] -= harga
        save_db(db)

    hasil = subprocess.getoutput(f"addzivpn {user} {pwd} {dur}")
    bot.send_message(msg.chat.id, hasil)

print("Bot aktif...")
bot.infinity_polling()
