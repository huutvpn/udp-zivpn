# ZiVPN Telegram Bot

Bot Telegram otomatis untuk membuat akun ZiVPN + sistem saldo + topup QRIS.

## Cara Install di VPS

Login sebagai root lalu jalankan:

cd /root
rm -rf udp-zivpn
git clone https://github.com/huutvpn/udp-zivpn.git
cd udp-zivpn
ls

Pastikan file berikut ada:

bot.py
config.py
requirements.txt
qris.jpg

## Install Dependencies

pip3 install -r requirements.txt

## Menjalankan Bot

python3 bot.py

Jika berhasil, bot akan aktif tanpa error.

## Konfigurasi

Edit file config.py

BOT_TOKEN = "ISI_TOKEN"
ADMIN_ID = 123456789

## Fitur

- Create akun otomatis
- Sistem saldo user
- Topup QRIS
- Admin bypass saldo
- Multi server support
