import telebot
import paramiko
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import *

bot = telebot.TeleBot(BOT_TOKEN)

def run_menu(choice):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(VPS_HOST, port=VPS_PORT, username=VPS_USER, password=VPS_PASSWORD)

        channel = ssh.invoke_shell()
        channel.send("bash /usr/local/bin/zi.sh\n")
        time.sleep(1)
        channel.send(choice + "\n")
        time.sleep(2)

        output = channel.recv(9999).decode()
        ssh.close()
        return output
    except Exception as e:
        return str(e)

def menu():
    m = InlineKeyboardMarkup(row_width=2)
    m.add(
        InlineKeyboardButton("➕ Buat Akun", callback_data="1"),
        InlineKeyboardButton("⏳ Trial Akun", callback_data="2"),
        InlineKeyboardButton("📊 Cek Server", callback_data="server"),
    )
    return m

@bot.message_handler(commands=['start'])
def start(msg):
    teks = f"""
👋 Hai, Member!

🆔 ID: {msg.from_user.id}
💰 Saldo: Rp 0
📌 Status: User

Silakan pilih menu:
"""
    bot.send_message(msg.chat.id, teks, reply_markup=menu())

@bot.callback_query_handler(func=lambda call: True)
def cb(call):
    if call.data == "server":
        hasil = run_menu("")
        bot.send_message(call.message.chat.id, "✅ Server OK")
    else:
        hasil = run_menu(call.data)
        bot.send_message(call.message.chat.id, f"Result:\n{hasil}")

print("Bot aktif...")
bot.infinity_polling()
