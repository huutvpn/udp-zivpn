import telebot
import subprocess
from config import *

bot = telebot.TeleBot(BOT_TOKEN)

user_data = {}

@bot.message_handler(commands=['start'])
def start(msg):
    bot.send_message(msg.chat.id, "👋 Selamat datang\nKirim /buat untuk membuat akun")

@bot.message_handler(commands=['buat'])
def buat(msg):
    user_data[msg.chat.id] = {}
    bot.send_message(msg.chat.id, "Masukkan Username:")
    bot.register_next_step_handler(msg, get_username)

def get_username(msg):
    user_data[msg.chat.id]['username'] = msg.text
    bot.send_message(msg.chat.id, "Masukkan Password:")
    bot.register_next_step_handler(msg, get_password)

def get_password(msg):
    user_data[msg.chat.id]['password'] = msg.text
    bot.send_message(msg.chat.id, "Masukkan Durasi (hari):")
    bot.register_next_step_handler(msg, get_duration)

def get_duration(msg):
    username = user_data[msg.chat.id]['username']
    password = user_data[msg.chat.id]['password']
    duration = msg.text

    cmd = f"addzivpn {username} {password} {duration}"
    result = subprocess.getoutput(cmd)

    bot.send_message(msg.chat.id, result)

print("Bot aktif...")
bot.infinity_polling()
