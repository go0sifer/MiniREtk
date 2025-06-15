#!/bin/bash

# Mini REtk Analyzer Automated Setup Script

set -e

# ====== USER CONFIG =======
USERNAME="go0se"
PROJECT_DIR="/home/$USERNAME/MiniREtk"
APP_SCRIPT="MiniREtk.py"
PDFID_SCRIPT="pdfid.py"
PDFPARSER_SCRIPT="pdf-parser.py"
LOGO_IMG="logo.gif"
BG_IMG="background.jpg"
PDFID_ZIP="pdfid_v0_2_10.zip"
PDFPARSER_ZIP="pdf-parser_V0_7_12.zip"
# ==========================

echo "---- Mini REtk Analyzer Automated Setup ----"

# 1. Update OS
echo "[*] Updating OS..."
sudo apt update && sudo apt upgrade -y

# 2. Install required packages
echo "[*] Installing Python, Flask, and forensic tools..."
sudo apt install -y python3 python3-flask python3-pip exiftool binutils file git dos2unix unzip

# 3. Create project directories
echo "[*] Creating project directories..."
mkdir -p "$PROJECT_DIR/uploads" "$PROJECT_DIR/archive" "$PROJECT_DIR/reports"

# 4. Check for required files
cd "$PROJECT_DIR"
missing=0

check_and_warn() {
    if [[ ! -f "$1" ]]; then
        if [[ "$1" == "$LOGO_IMG" || "$1" == "$BG_IMG" ]]; then
            echo "    [!] Optional: $1 not found. You can continue, but there will be no $( [[ "$1" == "$LOGO_IMG" ]] && echo "logo" || echo "background" )."
        else
            echo "    [!] Required: $1 is missing!"
            missing=1
        fi
    else
        echo "    [+] Found: $1"
    fi
}

echo "[*] Checking for required files in $PROJECT_DIR..."
check_and_warn "$APP_SCRIPT"
check_and_warn "$PDFID_ZIP"
check_and_warn "$PDFPARSER_ZIP"
check_and_warn "$LOGO_IMG"
check_and_warn "$BG_IMG"

if [[ $missing -eq 1 ]]; then
    echo
    echo "[!] One or more required files are missing. Please copy them to $PROJECT_DIR and press Enter to continue."
    read -p ""
    # Re-check after user input
    missing=0
    check_and_warn "$APP_SCRIPT"
    check_and_warn "$PDFID_ZIP"
    check_and_warn "$PDFPARSER_ZIP"
    if [[ $missing -eq 1 ]]; then
        echo "[!] Required files are still missing. Exiting setup."
        exit 1
    fi
fi

# 5. Unzip PDF tools if needed
echo "[*] Unzipping PDF tool archives..."
if [[ -f "$PDFID_ZIP" ]]; then
    unzip -o "$PDFID_ZIP"
fi
if [[ -f "$PDFPARSER_ZIP" ]]; then
    unzip -o "$PDFPARSER_ZIP"
fi

# 6. Convert line endings and make scripts executable
echo "[*] Converting line endings and setting executable permissions..."
dos2unix "$APP_SCRIPT" "$PDFID_SCRIPT" "$PDFPARSER_SCRIPT" || true
chmod +x "$APP_SCRIPT" "$PDFID_SCRIPT" "$PDFPARSER_SCRIPT" || true

# 7. Set up systemd service
echo "[*] Setting up systemd service..."
SERVICE_FILE="/etc/systemd/system/miniretk-analyzer.service"
sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Mini REtk Analyzer Service
After=network.target

[Service]
Type=simple
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

# 8. (Optional) Install AutoHotspot if running on Raspberry Pi
echo "[*] Checking if this is a Raspberry Pi for AutoHotspot install..."
if grep -q "Raspberry Pi" /proc/device-tree/model 2>/dev/null; then
    echo "[*] Raspberry Pi detected. Installing AutoHotspot..."
    curl "https://www.raspberryconnect.com/images/hsinstaller/Autohotspot-Setup.tar.xz" -o AutoHotspot-Setup.tar.xz
    tar -xvJf AutoHotspot-Setup.tar.xz
    cd Autohotspot
    sudo ./autohotspot-setup.sh
    cd ..
else
    echo "[*] Not a Raspberry Pi. Skipping AutoHotspot installation."
fi

echo
echo "---- Setup Complete ----"
echo "The Mini REtk Analyzer web interface should now be running on port 8080."
echo "Access it at: http://<device-ip>:8080"
echo "If no WiFi is available, connect to the Pi's hotspot and use the Pi's hotspot IP address."
echo "To check the Mini REtk Analyzer service: sudo systemctl status miniretk-analyzer"
echo "To check AutoHotspot: sudo systemctl status autohotspot"
echo
echo "Enjoy using Mini REtk Analyzer!"
