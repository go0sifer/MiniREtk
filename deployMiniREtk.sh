#!/bin/bash

# Mini REtk Analyzer Automated Setup Script

set -e

# ====== USER CONFIG =======
USERNAME="go0se"
PROJECT_DIR="/home/$USERNAME"
APP_SCRIPT="MiniREtk.py"
PDFID_SCRIPT="pdfid.py"
PDFPARSER_SCRIPT="pdf-parser.py"
LOGO_IMG="logo.jpg"
BG_IMG="background.jpg"
# ==========================

echo "---- Mini REtk Analyzer Automated Setup ----"

# 1. Update OS
echo "[*] Updating OS..."
sudo apt update && sudo apt upgrade -y

# 2. Install required packages
echo "[*] Installing Python, Flask, and forensic tools..."
sudo apt install -y python3 python3-flask python3-pip exiftool binutils file git dos2unix

# 3. Create project directories
echo "[*] Creating project directories..."
mkdir -p "$PROJECT_DIR/uploads" "$PROJECT_DIR/archive" "$PROJECT_DIR/reports"

# 4. Prompt for copying scripts and images
echo "[*] Please copy your $APP_SCRIPT, $PDFID_SCRIPT, $PDFPARSER_SCRIPT, $LOGO_IMG, and $BG_IMG to $PROJECT_DIR."
echo "    You can use scp or any other method."
read -p "Press Enter to continue after copying the files..."

# 5. Convert line endings and make scripts executable
echo "[*] Converting line endings and setting executable permissions..."
cd "$PROJECT_DIR"
dos2unix "$APP_SCRIPT" "$PDFID_SCRIPT" "$PDFPARSER_SCRIPT" || true
chmod +x "$APP_SCRIPT" "$PDFID_SCRIPT" "$PDFPARSER_SCRIPT" || true

# 6. Set up systemd service
echo "[*] Setting up systemd service..."
SERVICE_FILE="/etc/systemd/system/miniretk-analyzer.service"
sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Mini REtk Analyzer Flask App
After=network.target

[Service]
User=$USERNAME
WorkingDirectory=$PROJECT_DIR
ExecStart=/usr/bin/python3 $PROJECT_DIR/$APP_SCRIPT
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable miniretk-analyzer
sudo systemctl restart miniretk-analyzer

echo "[*] Mini REtk Analyzer service installed and started."

# 7. Install and configure AutoHotspot (GitHub method)
echo "[*] Installing AutoHotspot for fallback WiFi access point from GitHub..."
cd "$PROJECT_DIR"
if [ ! -d AutoHotspot-Installer ]; then
    git clone https://github.com/RaspberryConnect/AutoHotspot-Installer.git
fi
cd AutoHotspot-Installer/AutoHotspot-Setup/Autohotspot
sudo chmod +x autohotspot-setup.sh
sudo ./autohotspot-setup.sh

echo "[*] AutoHotspot installed. You can edit /etc/hostapd/hostapd.conf to change SSID and password if desired."

# 8. Final message
echo
echo "---- Mini REtk Analyzer Setup Complete! ----"
echo "Access the web app at http://<raspberrypi-ip>:8080"
echo "If no WiFi is available, connect to the Pi's hotspot and use the Pi's hotspot IP address."
echo "To check the Mini REtk Analyzer service: sudo systemctl status miniretk-analyzer"
echo "To check AutoHotspot: sudo systemctl status autohotspot"
echo
echo "Enjoy using Mini REtk Analyzer!"
