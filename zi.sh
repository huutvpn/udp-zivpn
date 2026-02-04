#!/bin/bash
set -e

clear
echo "======================================="
echo "   UDP ZIVPN Installer - leryyvpn"
echo "======================================="

# ====== VAR ======
REPO="leryyvpn/udp-zivpn"
BIN_DIR="/usr/local/bin"
CONF_DIR="/etc/zivpn"
BIN_NAME="udp-zivpn"

mkdir -p $CONF_DIR

# ====== DETECT ARCH ======
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

# ====== DOWNLOAD BINARY (FALLBACK SAFE) ======
URL="https://github.com/$REPO/releases/latest/download/$FILE"

echo "📥 Download binary: $FILE"
wget -q --show-progress -O $BIN_DIR/$BIN_NAME "$URL"

if [[ ! -f $BIN_DIR/$BIN_NAME ]]; then
  echo "❌ Gagal download binary"
  exit 1
fi

chmod +x $BIN_DIR/$BIN_NAME

# ====== CONFIG ======
if [[ ! -f $CONF_DIR/config.json ]]; then
cat > $CONF_DIR/config.json <<EOF
{
  "listen": ":36712",
  "log": "info"
}
EOF
fi

# ====== SERVICE ======
cat >/etc/systemd/system/zivpn.service <<EOF
[Unit]
Description=UDP ZIVPN Service
After=network.target

[Service]
Type=simple
ExecStart=$BIN_DIR/$BIN_NAME -c $CONF_DIR/config.json
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
echo "📌 Repo  : $REPO"
echo "📌 Port  : 36712"
echo "📌 Service: zivpn"
echo