# ✅ ZiVPN Telegram Bot – Panduan Instalasi

## ✅ 1. Masuk root & bersihkan folder lama

```bash
cd /root
rm -rf udp-zivpn
```

---

## ✅ 2. Clone repository

```bash
git clone https://github.com/huutvpn/udp-zivpn.git
cd udp-zivpn
ls
```

WAJIB muncul file berikut:

bot.py
config.py
requirements.txt
qris.jpg

Kalau file belum ada → berarti repo GitHub belum ke-update.

---

## ✅ 3. Install Python module

```bash
pip3 install -r requirements.txt
```

---

## ✅ 4. Jalankan bot

```bash
python3 bot.py
```

Kalau benar → bot langsung online & tidak ada error merah.

---

## ⚠️ Jika muncul error

❌ requirements.txt not found  
Berarti kamu belum masuk folder repo

```bash
cd /root/udp-zivpn
ls
```

❌ bot.py not found  
Artinya kamu menjalankan command di folder yang salah

```bash
pwd
```

Harusnya:

/root/udp-zivpn

---

## ✅ Tips Anti Error

Jalankan full command ini:

```bash
cd /root
rm -rf udp-zivpn
git clone https://github.com/huutvpn/udp-zivpn.git
cd udp-zivpn
pip3 install -r requirements.txt
python3 bot.py
```
