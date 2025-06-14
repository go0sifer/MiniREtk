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

## **Deploy**
 - If you want to run MiniREtk see delpoyMiniREtk.sh. You'll have to go get pdfid.py and pdf-parser.py on your own.
