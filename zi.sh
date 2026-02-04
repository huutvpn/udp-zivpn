#!/bin/bash
set -e

clear
echo "======================================"
echo "   UDP ZIVPN Installer (huutvpn)"
echo "======================================"

# ===== VAR =====
REPO="huutvpn/udp-zivpn"
BIN_NAME="udp-zivpn"
BIN_PATH="/usr/local/bin/$BIN_NAME"
CONF_DIR="/etc/zivpn"
CONF_FILE="$CONF_DIR/config.json"

mkdir -p $CONF_DIR

# ===== DETECT ARCH =====
ARCH=$(uname -m)
case "$ARCH" in
  x86_64)
    FILE="udp-zivpn-linux-amd64"
    ;;
  aarch64)
    FILE="udp-zivpn-linux-arm64"
    ;;
  arm*)
    FILE="udp-zivpn-linux-arm"
    ;;
  *)
    echo "❌ Arsitektur tidak didukung: $ARCH"
    exit 1
    ;;
esac

# ===== DOWNLOAD =====
URL="https://github.com/$REPO/releases/latest/download/$FILE"
echo "📥 Download: $URL"

wget -O "$BIN_PATH" "$URL"

chmod +x "$BIN_PATH"

# ===== CONFIG =====
if [[ ! -f $CONF_FILE ]]; then
cat > "$CONF_FILE" <<EOF
{
  "listen": ":36712",
  "log": "info"
}
EOF
fi

# ===== SYSTEMD =====
cat > /etc/systemd/system/zivpn.service <<EOF
[Unit]
Description=UDP ZIVPN Service
After=network.target

[Service]
Type=simple
ExecStart=$BIN_PATH -c $CONF_FILE
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reexec
systemctl daemon-reload
systemctl enable zivpn
systemctl restart zivpn

echo
echo "✅ UDP ZIVPN BERHASIL TERPASANG"
echo "📌 Repo : $REPO"
echo "📌 Port : 36712"
echo "📌 Cek  : systemctl status zivpn"
echo