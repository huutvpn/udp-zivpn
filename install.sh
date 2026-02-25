#!/bin/bash

echo "Installing ZiVPN + Telegram Bot..."

# Move zi.sh
if [ -f zi.sh ]; then
    chmod +x zi.sh
    mv zi.sh /usr/local/bin/zi.sh
    chmod +x /usr/local/bin/zi.sh
fi

# Permissions
chmod +x *.sh 2>/dev/null

# Dependencies
apt update -y
apt install python3 python3-pip screen -y

pip3 install pyTelegramBotAPI paramiko

echo "Installation complete!"
echo "Run bot with:"
echo "python3 bot.py"
