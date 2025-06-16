```
                                          _____        _____                    
 ______  _____  _____  ______  ______  __|__   |__  __|___  |__    __    __  __ 
|   ___|/     \/     ||   ___||   ___||     |     ||   ___|    | _|  |_ |  |/ / 
|   |  ||     ||  /  | `-.`-. |   ___||     \     ||   ___|    ||_    _||     \ 
|______|\_____/|_____/|______||______||__|\__\  __||______|  __|  |__|  |__|\__\
                                         |_____|      |_____|                   
01100111 01101111 00110000 01110011 01100101 01010010 01000101 01110100 01101011  
```
## 📝 **Summary: Mini REtk Analyzer**

**Mini REtk Analyzer** is a web-based forensic file analysis platform built with Flask. It allows users to upload files, analyze them with common forensic tools, archive/unarchive files, and generate detailed, deduplicated per-file reports. The tool is designed for security analysts, incident responders, and forensic investigators.

### **Key Features**
- **File Uploads:** Upload any file for analysis. (Note: Original file system timestamps cannot be preserved via browser upload.)
- **Analysis Tools:** Run `pdfid.py`, `pdf-parser.py`, `exiftool`, `file`, and `strings` on any file with a single click.
- **Hashing:** Computes and displays MD5, SHA1, SHA256, and SHA512 hashes for each file.
- **File Metadata:** Reports include file size (bytes and human-readable), MIME type, extension, entropy, and original upload path.
- **VirusTotal Link:** Each report includes a direct VirusTotal scan link using the SHA256 hash.
- **Archiving:** Move files in and out of an archive area for better workflow management.
- **Per-file Reports:** Each file has its own `.report.txt` file, which logs all unique analysis results with timestamps and prevents duplicate entries.
- **Web UI:** Modern, responsive interface with SVG icons, download links, and quick access to all features.
- **No Data Loss:** Deleting a file from the UI also deletes its analysis report.
- **Automatic startup** via systemd service.
- **Automatic WiFi Access Point setup:** If the device cannot connect to a known WiFi network on boot, it will automatically create its own WiFi access point (hotspot), allowing direct connection to the device and access to the web app. This ensures you can always connect to Mini REtk, even in environments without existing WiFi.

### **Workflow**
1. **Upload a file.**
2. **Analyze:** Click any tool button to run an analysis. Output is shown on-screen and appended to the report (deduplicated).
3. **Archive/Unarchive:** Move files in/out of the archive as needed.
4. **Reports:** Download or view detailed per-file reports at any time.

### **Speedrun**
 - View the speedrun of the app here: https://youtu.be/Dl0Pyo-j40A

## **Deploy**

### **Quick Start**

1. **Download Required Files**
   - Download `deployMiniREtk.sh`, `MiniREtk.py`, `pdfid.py`, and `pdf-parser.py`.
   - Obtain or create your images: `background.jpg` and `logo.gif`. (Or use the ones supplied)

2. **Make the Installer Executable**
   ```bash
   chmod +x deployMiniREtk.sh
   ```

3. **Edit User Configuration (Required)**
   - **Before running the installer**, update the configuration at the top of both `deployMiniREtk.sh` and `MiniREtk.py` to match your system’s username and confirm the installation directory.

---

## **Configuration Instructions**

### **1. Update Username and Paths**

#### **In `deployMiniREtk.sh`:**

At the top of the script, you will see:
```bash
# ====== USER CONFIG =======
USERNAME="go0se"
PROJECT_DIR="/home/$USERNAME/MiniREtk"
APP_SCRIPT="MiniREtk.py"
PDFID_SCRIPT="pdfid.py"
PDFPARSER_SCRIPT="pdf-parser.py"
LOGO_IMG="logo.gif"
BG_IMG="background.jpg"
# ==========================
```
- **Change `USERNAME`** to your system username (e.g., `"yourusername"`).
- **`PROJECT_DIR`** is now set to `/home/$USERNAME/MiniREtk` by default. Change only if you want a different location.

#### **In `MiniREtk.py`:**

At the top, look for:
```python
# ====== USER CONFIG =======
USERNAME = "go0se"
PROJECT_DIR = f"/home/{USERNAME}/MiniREtk"
UPLOAD_FOLDER = f"{PROJECT_DIR}/uploads"
ARCHIVE_FOLDER = f"{PROJECT_DIR}/archive"
REPORTS_FOLDER = f"{PROJECT_DIR}/reports"
LOGO_PATH = f"{PROJECT_DIR}/logo.gif"
BG_PATH = f"{PROJECT_DIR}/background.jpg"
PDFID_PATH = f"{PROJECT_DIR}/pdfid.py"
PDFPARSER_PATH = f"{PROJECT_DIR}/pdf-parser.py"
EXIFTOOL_PATH = 'exiftool'
# ==========================
```
- **Change `USERNAME`** to match what you set in the shell script.
- **`PROJECT_DIR`** should be `/home/yourusername/MiniREtk` unless you have a reason to change it.

> **Both files must use the same username and project directory.**

---

### **2. Run the Installer**

- Execute the installer:
  ```bash
  ./deployMiniREtk.sh
  ```
- The script will:
  - Update your OS and install dependencies.
  - Create the project directory at `/home/$USERNAME/MiniREtk` and its subfolders.
  - Prompt you to copy scripts and images into the project directory.
  - Convert line endings and set executable permissions.
  - Set up the systemd service for automatic startup.

---

### **3. Copy Required Files**

- When prompted, copy the following into your project directory (`/home/yourusername/MiniREtk/`):
  - `MiniREtk.py`
  - `pdfid.py`
  - `pdf-parser.py`
  - `logo.gif`
  - `background.jpg`

---

### **4. Final Steps**

- The script will finish setup and provide instructions for accessing the web interface.
- For Raspberry Pi, it will attempt to set up AutoHotspot for WiFi fallback (this step will fail gracefully on non-Raspberry Pi systems).

---

## **Summary Table: Where to Edit Configs**

| File             | Variable(s) to Edit   | Example Value                    | Purpose                      |
|------------------|----------------------|----------------------------------|------------------------------|
| deployMiniREtk.sh| USERNAME, PROJECT_DIR| "yourusername", "/home/yourusername/MiniREtk" | Sets install location        |
| MiniREtk.py      | USERNAME, PROJECT_DIR| "yourusername", "/home/yourusername/MiniREtk" | Sets runtime paths           |

---

## **Additional Notes**

- Download `pdfid.py` and `pdf-parser.py` from Didier Stevens’ blog. https://blog.didierstevens.com/programs/pdf-tools/
- Use your own images for `background.jpg` and `logo.gif`.
- The default install location is now `/home/$USERNAME/MiniREtk`.
- The application runs headless and is accessible via browser on port 8080 of the device.
