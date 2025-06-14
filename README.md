## 📝 **Summary: Mini Analyzer Tool**

**Mini Analyzer** is a web-based forensic file analysis platform built with Flask. It allows users to upload files, analyze them with common forensic tools, archive/unarchive files, and generate detailed, deduplicated per-file reports. The tool is designed for security analysts, incident responders, and forensic investigators.

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

### **Workflow**
1. **Upload a file.**
2. **Analyze:** Click any tool button to run an analysis. Output is shown on-screen and appended to the report (deduplicated).
3. **Archive/Unarchive:** Move files in/out of the archive as needed.
4. **Reports:** Download or view detailed per-file reports at any time.
