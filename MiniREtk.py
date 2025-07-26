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
EXIFTOOL_PATH = "exiftool"
# ==========================

import glob
import hashlib
import math
import os
import shutil
import subprocess
import tempfile
from datetime import datetime

from flask import (Flask, redirect, render_template_string, request,
                   send_from_directory, url_for)
from werkzeug.utils import secure_filename

app = Flask(__name__)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ARCHIVE_FOLDER, exist_ok=True)
os.makedirs(REPORTS_FOLDER, exist_ok=True)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Mini REtk Analyzer</title>
    <link href="https://fonts.googleapis.com/css?family=Montserrat:700,400&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Montserrat', sans-serif; background: url('/background.jpg') no-repeat center center fixed; background-size: cover; color: #f3f3f3; margin: 0; min-height: 100vh;}
        .container { max-width: 900px; margin: 40px auto 0 auto; background: rgba(30, 30, 48, 0.97); border-radius: 18px; box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37); padding: 32px 36px 36px 36px; }
        .logo { display: block; margin: 0 auto 20px auto; width: 120px; border-radius: 12px; box-shadow: 0 2px 8px #0008; }
        .top-buttons { display: flex; justify-content: flex-end; margin-bottom: 12px; }
        .top-buttons a { margin-left: 8px; }
        .top-btn, .archive-btn, .reports-btn { background: linear-gradient(90deg, #16a34a 0%, #22c55e 100%); color: #232323; border: none; border-radius: 8px; padding: 8px 18px; font-size: 1rem; font-weight: 600; cursor: pointer; box-shadow: 0 2px 8px #0004; text-decoration: none; display: inline-flex; align-items: center; gap: 7px; }
        .top-btn:hover, .archive-btn:hover, .reports-btn:hover { background: linear-gradient(90deg, #22c55e 0%, #65a30d 100%); color: #232323; text-decoration: none; }
        h1 { text-align: center; font-weight: 700; letter-spacing: 1px; margin-bottom: 8px; }
        h2 { margin-top: 36px; font-weight: 700; color: #006600; }
        form.upload-form { display: flex; justify-content: center; align-items: center; gap: 12px; margin-bottom: 22px; }
        input[type="file"] { color: #fff; }
        input[type="submit"], button, .icon-btn-link { background: linear-gradient(90deg, #16a34a 0%, #22c55e 100%); color: #232323; border: none; border-radius: 8px; padding: 8px; font-size: 1.1rem; font-weight: 600; cursor: pointer; margin-left: 8px; transition: box-shadow 0.2s, background 0.2s; box-shadow: 0 2px 8px #0004; display: flex; align-items: center; justify-content: center; text-decoration: none; min-width: 38px; min-height: 38px; }
        input[type="submit"]:hover, button:hover, .icon-btn-link:hover { background: linear-gradient(90deg, #22c55e 0%, #65a30d 100%); box-shadow: 0 4px 16px #0006; color: #232323; text-decoration: none; }
        .hash-btn { min-width: 38px; min-height: 38px; padding: 8px; background: linear-gradient(90deg, #16a34a 0%, #22c55e 100%); color: #232323; border: none; font-size: 0.9rem; font-family: monospace; font-weight: 600; border-radius: 8px; margin-left: 8px; text-decoration: none; }
        .hash-btn:hover { background: linear-gradient(90deg, #22c55e 0%, #65a30d 100%); color: #232323; }
        ul { list-style: none; padding: 0; }
        li { background: rgba(255,255,255,0.04); margin: 10px 0; padding: 12px 16px; border-radius: 10px; display: flex; align-items: center; justify-content: space-between; }
        li a.filename-link { color: #00cc00; font-weight: 600; text-decoration: none; margin-right: 18px; flex-grow: 1; word-break: break-all; }
        li a.filename-link:hover { text-decoration: underline; }
        .button-group { display: flex; gap: 8px; flex-shrink: 0; }
        .icon-btn { width: 22px; height: 22px; vertical-align: middle; display: block; margin: 0; color: #232323; transition: color 0.2s; }
        .delete-btn .icon-btn { color: #e11d48; }
        .archive-btn .icon-btn { color: #232323; }
        .reports-btn .icon-btn { color: #3300cc; }
        .icon-btn:hover { color: #cc0000; }
        pre { background: #23233a; color: #fffde7; border-radius: 8px; padding: 18px; margin-top: 20px; overflow-x: auto; font-size: 1em; white-space: pre-wrap; word-break: break-word; }
        @media (max-width: 900px) { .container { padding: 10px; } li { flex-direction: column; align-items: flex-start; } .button-group { margin-top: 8px; } }
    </style>
</head>
<body>
    <div class="container">
        <img src="/logo.gif" class="logo" alt="Logo">
        <div class="top-buttons">
            {% if not archive and not reports %}
                <a href="/archive" class="archive-btn" title="View Archive">
                    <svg class="icon-btn" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4 4h16v2H4zm2 4h12v10a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2z" stroke-width="2"/></svg>
                    Archive
                </a>
                <a href="/reports" class="reports-btn" title="View Reports">
                    <svg class="icon-btn" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="2" stroke-width="2"/><text x="12" y="16" font-size="10" fill="currentColor" text-anchor="middle" font-family="monospace">R</text></svg>
                    Reports
                </a>
            {% elif archive %}
                <a href="/" class="top-btn" title="Back to Analysis">
                    <svg class="icon-btn" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M15 19l-7-7 7-7" stroke-width="2"/></svg>
                    Back
                </a>
                <a href="/reports" class="reports-btn" title="View Reports">
                    <svg class="icon-btn" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="2" stroke-width="2"/><text x="12" y="16" font-size="10" fill="currentColor" text-anchor="middle" font-family="monospace">R</text></svg>
                    Reports
                </a>
            {% elif reports %}
                <a href="/" class="top-btn" title="Back to Analysis">
                    <svg class="icon-btn" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M15 19l-7-7 7-7" stroke-width="2"/></svg>
                    Back
                </a>
                <a href="/archive" class="archive-btn" title="View Archive">
                    <svg class="icon-btn" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4 4h16v2H4zm2 4h12v10a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2z" stroke-width="2"/></svg>
                    Archive
                </a>
            {% endif %}
        </div>
        <h1>Mini REtk Analyzer</h1>
        {% if not archive and not reports %}
        <form class="upload-form" method="post" enctype="multipart/form-data">
            <input type="file" name="file" required>
            <input type="submit" value="Upload">
        </form>
        {% endif %}
        <h2>
            {% if archive %}
                Archived Files
            {% elif reports %}
                Reports
            {% else %}
                Uploaded Files
            {% endif %}
        </h2>
        <ul>
        {% for file in files %}
            <li>
                {% if reports %}
                    <a class="filename-link" href="/reportsfile/{{file}}" target="_blank">{{file}}</a>
                    <a class="icon-btn-link" href="/reportsfile/{{file}}" download title="Download Report">
                        <svg class="icon-btn" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M5 20h14a1 1 0 0 0 1-1v-4h-2v3H6v-3H4v4a1 1 0 0 0 1 1zm7-2V4h-2v14l-5-5-1.41 1.41L12 22l7.41-7.41L18 14l-5 5z" stroke-width="2"/></svg>
                    </a>
                {% elif archive %}
                    <a class="filename-link" href="/archivefile/{{file}}" target="_blank">{{file}}</a>
                {% else %}
                    <span class="filename-link">{{file}}</span>
                {% endif %}
                <div class="button-group">
                {% if not archive and not reports and file.lower().endswith('.pdf') %}
                    <form style="display:inline;" method="post" action="/run/pdfid/{{file}}">
                        <button type="submit" title="Run pdfid.py">
                            <svg class="icon-btn" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="10" cy="10" r="7" stroke-width="2"/><line x1="15" y1="15" x2="21" y2="21" stroke-width="2"/></svg>
                        </button>
                    </form>
                    <form style="display:inline;" method="post" action="/run/pdfparser/{{file}}">
                        <button type="submit" title="Run pdf-parser.py">
                            <svg class="icon-btn" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" viewBox="0 0 24 24"><rect x="4" y="2" width="16" height="20" rx="2" stroke-width="2"/><line x1="8" y1="6" x2="16" y2="6" stroke-width="2"/><line x1="8" y1="10" x2="16" y2="10" stroke-width="2"/><line x1="8" y1="14" x2="12" y2="14" stroke-width="2"/></svg>
                        </button>
                    </form>
                    <form style="display:inline;" method="post" action="/generate_pdf_image/{{file}}">
                      <button type="submit" title="Generate Preview Images">
                        <svg class="icon-btn" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <rect x="5" y="5" width="14" height="14" rx="2" stroke="currentColor" stroke-width="2" fill="none"/>
                          <text x="12" y="16" font-size="8" fill="currentColor" text-anchor="middle" font-family="monospace">IMG</text>
                        </svg>
                      </button>
                    </form>
                {% endif %}
                {% if not reports %}
                    <form style="display:inline;" method="post" action="/run/exiftool/{{file}}">
                        <button type="submit" title="Run exiftool">
                            <svg class="icon-btn" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" stroke-width="2"/><circle cx="12" cy="12" r="4" stroke-width="2"/></svg>
                        </button>
                    </form>
                    <form style="display:inline;" method="post" action="/run/filecmd/{{file}}">
                        <button type="submit" title="Run file command">
                            <svg class="icon-btn" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <rect x="4" y="4" width="16" height="16" rx="2" stroke-width="2"/>
                                <text x="12" y="16" font-size="10" fill="currentColor" text-anchor="middle" font-family="monospace">F</text>
                            </svg>
                        </button>
                    </form>
                    <form style="display:inline;" method="post" action="/run/strings/{{file}}">
                        <button type="submit" title="Run strings">
                            <svg class="icon-btn" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <rect x="4" y="4" width="16" height="16" rx="2" stroke-width="2"/>
                                <text x="12" y="16" font-size="10" fill="currentColor" text-anchor="middle" font-family="monospace">S</text>
                            </svg>
                        </button>
                    </form>
                {% endif %}
                {% if not reports %}
                    <a class="icon-btn-link" href="{{ '/archivefile/' + file if archive else '/uploads/' + file }}" download title="Download">
                        <svg class="icon-btn" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M5 20h14a1 1 0 0 0 1-1v-4h-2v3H6v-3H4v4a1 1 0 0 0 1 1zm7-2V4h-2v14l-5-5-1.41 1.41L12 22l7.41-7.41L18 14l-5 5z" stroke-width="2"/></svg>
                    </a>
                {% endif %}
                {% if not reports and not archive %}
                    <form style="display:inline;" method="post" action="/archive/{{file}}">
                        <button type="submit" title="Archive" class="archive-btn">
                            <svg class="icon-btn" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M4 4h16v2H4zm2 4h12v10a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2z" stroke-width="2"/></svg>
                        </button>
                    </form>
                {% elif archive %}
                    <form style="display:inline;" method="post" action="/unarchive/{{file}}">
                        <button type="submit" title="Unarchive" class="archive-btn">
                            <svg class="icon-btn" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M20 20H4V4h16v16zm-8-4v-6m0 6l-3-3m3 3l3-3" stroke-width="2"/></svg>
                        </button>
                    </form>
                {% endif %}
                <form style="display:inline;" method="post" action="{{ '/delete_archive/' + file if archive else '/delete/' + file if not reports else '/delete_report/' + file }}" onsubmit="return confirm('Are you sure you want to delete {{file}}?');">
                    <button type="submit" title="Delete" class="delete-btn">
                        <svg class="icon-btn" xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" viewBox="0 0 24 24"><rect x="5" y="5" width="14" height="14" rx="2" stroke-width="2"/><line x1="9" y1="9" x2="15" y2="15" stroke-width="2"/><line x1="15" y1="9" x2="9" y2="15" stroke-width="2"/></svg>
                    </button>
                </form>
                {% if not reports and not archive %}
                    <a class="hash-btn" href="https://www.virustotal.com/gui/file/{{hashes[file]}}" target="_blank" title="Lookup on VirusTotal">{{hashes[file][:8]}}…</a>
                {% endif %}
                </div>
            </li>
        {% endfor %}
        </ul>
        {% if output %}
          <h2>Script Output</h2>
          <pre>{{output|safe}}</pre>
        {% endif %}
    </div>
</body>
</html>
"""


def md5sum(filepath):
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def sha1sum(filepath):
    h = hashlib.sha1()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256sum(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def sha512sum(filepath):
    h = hashlib.sha512()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def human_readable_size(size, decimal_places=1):
    for unit in ["bytes", "KB", "MB", "GB", "TB"]:
        if size < 1024.0:
            return f"{size:.{decimal_places}f} {unit}"
        size /= 1024.0
    return f"{size:.{decimal_places}f} PB"


def calculate_entropy(filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    if not data:
        return 0.0
    entropy = 0
    length = len(data)
    for x in range(256):
        p_x = data.count(x) / length
        if p_x > 0:
            entropy += -p_x * math.log2(p_x)
    return entropy


def get_file_details(filepath):
    size = os.path.getsize(filepath)
    human_size = human_readable_size(size)
    ext = os.path.splitext(filepath)[1]
    try:
        mime_type = subprocess.check_output(
            ["file", "--mime-type", "-b", filepath], universal_newlines=True
        ).strip()
    except Exception:
        mime_type = "unknown"
    entropy = calculate_entropy(filepath)
    return size, human_size, mime_type, ext, entropy


def get_report_path(filename):
    return os.path.join(REPORTS_FOLDER, f"{filename}.report.txt")


def append_to_report(script, filename, output):
    report_path = get_report_path(filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    original_path = file_path
    if not os.path.isfile(file_path):
        file_path = os.path.join(ARCHIVE_FOLDER, filename)
        original_path = file_path
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not os.path.exists(report_path):
        size, human_size, mime_type, ext, entropy = get_file_details(file_path)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(f"=== REPORT FOR: {filename} ===\n")
            f.write(f"MD5:     {md5sum(file_path)}\n")
            f.write(f"SHA1:    {sha1sum(file_path)}\n")
            f.write(f"SHA256:  {sha256sum(file_path)}\n")
            f.write(f"SHA512:  {sha512sum(file_path)}\n")
            f.write(f"File size: {size} bytes ({human_size})\n")
            f.write(f"MIME type: {mime_type}\n")
            f.write(f"Extension: {ext}\n")
            f.write(f"Entropy: {entropy:.4f}\n")
            f.write(f"Original upload path: {original_path}\n")
            f.write(
                f"VirusTotal: https://www.virustotal.com/gui/file/{sha256sum(file_path)}\n"
            )
            f.write(f"First Analysis: {now}\n")
            f.write("=" * 40 + "\n")

    file_hash = sha256sum(file_path) if os.path.isfile(file_path) else "N/A"
    unique_block = f"SCRIPT: {script}\nFILE: {filename}\nHASH: {file_hash}\n---\n"
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()
        if unique_block in content:
            return

    header = (
        f"\n--- {now} ---\nSCRIPT: {script}\nFILE: {filename}\nHASH: {file_hash}\n---\n"
    )
    with open(report_path, "a", encoding="utf-8") as f:
        f.write(header)
        f.write(output)
        f.write("\n")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" in request.files:
            file = request.files["file"]
            if file.filename:
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                return redirect(url_for("index"))

    files = [
        f
        for f in os.listdir(UPLOAD_FOLDER)
        if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))
    ]
    hashes = {f: sha256sum(os.path.join(UPLOAD_FOLDER, f)) for f in files}
    return render_template_string(
        HTML_TEMPLATE,
        files=files,
        output=None,
        hashes=hashes,
        archive=False,
        reports=False,
    )


@app.route("/archive")
def view_archive():
    files = [
        f
        for f in os.listdir(ARCHIVE_FOLDER)
        if os.path.isfile(os.path.join(ARCHIVE_FOLDER, f))
    ]
    return render_template_string(
        HTML_TEMPLATE, files=files, output=None, hashes={}, archive=True, reports=False
    )


@app.route("/reports")
def view_reports():
    files = [
        f
        for f in os.listdir(REPORTS_FOLDER)
        if os.path.isfile(os.path.join(REPORTS_FOLDER, f))
    ]
    return render_template_string(
        HTML_TEMPLATE, files=files, output=None, hashes={}, archive=False, reports=True
    )


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    filename = secure_filename(filename)
    return send_from_directory(UPLOAD_FOLDER, filename)


@app.route("/archivefile/<filename>")
def archive_file(filename):
    filename = secure_filename(filename)
    return send_from_directory(ARCHIVE_FOLDER, filename)


@app.route("/reportsfile/<filename>")
def report_file(filename):
    filename = secure_filename(filename)
    return send_from_directory(REPORTS_FOLDER, filename)


@app.route("/logo.gif")
def logo():
    return send_from_directory(PROJECT_DIR, "logo.gif")


@app.route("/background.jpg")
def background():
    return send_from_directory(PROJECT_DIR, "background.jpg")


@app.route("/run/<script>/<filename>", methods=["POST"])
def run_script(script, filename):
    filename = secure_filename(filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.isfile(filepath):
        return "File not found", 404

    output = None
    if script == "pdfid":
        command = ["python3", PDFID_PATH, filepath]
    elif script == "pdfparser":
        command = ["python3", PDFPARSER_PATH, "-c", filepath]
    elif script == "exiftool":
        command = [EXIFTOOL_PATH, filepath]
    elif script == "filecmd":
        command = ["file", filepath]
    elif script == "strings":
        command = ["strings", filepath]
    else:
        output = "Invalid script"

    if output is None:
        try:
            output = subprocess.check_output(
                command,
                stderr=subprocess.STDOUT,
                timeout=300,
                universal_newlines=True,
            )
            append_to_report(script, filename, output)
        except subprocess.CalledProcessError as e:
            output = f"Error: {e.output}"
        except Exception as e:
            output = str(e)

    files = [
        f
        for f in os.listdir(UPLOAD_FOLDER)
        if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))
    ]
    hashes = {f: sha256sum(os.path.join(UPLOAD_FOLDER, f)) for f in files}
    return render_template_string(
        HTML_TEMPLATE,
        files=files,
        output=output,
        hashes=hashes,
        archive=False,
        reports=False,
    )


@app.route("/run_archive/strings/<filename>", methods=["POST"])
def run_archive_strings(filename):
    filename = secure_filename(filename)
    filepath = os.path.join(ARCHIVE_FOLDER, filename)
    if not os.path.isfile(filepath):
        return "File not found", 404
    try:
        output = subprocess.check_output(
            ["strings", filepath],
            stderr=subprocess.STDOUT,
            timeout=300,
            universal_newlines=True,
        )
        append_to_report("strings", filename, output)
    except subprocess.CalledProcessError as e:
        output = f"Error: {e.output}"
    except Exception as e:
        output = str(e)
    files = [
        f
        for f in os.listdir(ARCHIVE_FOLDER)
        if os.path.isfile(os.path.join(ARCHIVE_FOLDER, f))
    ]
    return render_template_string(
        HTML_TEMPLATE,
        files=files,
        output=output,
        hashes={},
        archive=True,
        reports=False,
    )


@app.route("/archive/<filename>", methods=["POST"])
def archive(filename):
    filename = secure_filename(filename)
    src = os.path.join(UPLOAD_FOLDER, filename)
    dst = os.path.join(ARCHIVE_FOLDER, filename)
    if os.path.isfile(src):
        shutil.move(src, dst)
        out_txt_src = src + ".out.txt"
        out_txt_dst = dst + ".out.txt"
        if os.path.isfile(out_txt_src):
            shutil.move(out_txt_src, out_txt_dst)
    return redirect(url_for("index"))


@app.route("/unarchive/<filename>", methods=["POST"])
def unarchive(filename):
    filename = secure_filename(filename)
    src = os.path.join(ARCHIVE_FOLDER, filename)
    dst = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.isfile(src):
        shutil.move(src, dst)
        out_txt_src = src + ".out.txt"
        out_txt_dst = dst + ".out.txt"
        if os.path.isfile(out_txt_src):
            shutil.move(out_txt_src, out_txt_dst)
    return redirect(url_for("view_archive"))


@app.route("/delete/<filename>", methods=["POST"])
def delete_file(filename):
    filename = secure_filename(filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)
        outpath = filepath + ".out.txt"
        if os.path.isfile(outpath):
            os.remove(outpath)
        report_path = os.path.join(REPORTS_FOLDER, f"{filename}.report.txt")
        if os.path.isfile(report_path):
            os.remove(report_path)
    return redirect(url_for("index"))


@app.route("/delete_archive/<filename>", methods=["POST"])
def delete_archive_file(filename):
    filename = secure_filename(filename)
    filepath = os.path.join(ARCHIVE_FOLDER, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)
        outpath = filepath + ".out.txt"
        if os.path.isfile(outpath):
            os.remove(outpath)
        report_path = os.path.join(REPORTS_FOLDER, f"{filename}.report.txt")
        if os.path.isfile(report_path):
            os.remove(report_path)
    return redirect(url_for("view_archive"))


@app.route("/delete_report/<path:filename>", methods=["POST"])
def delete_report_file_route(filename):
    filename = secure_filename(filename)
    report_path = os.path.join(REPORTS_FOLDER, filename)
    if os.path.isfile(report_path):
        os.remove(report_path)
    return redirect(url_for("view_reports"))


@app.route("/generate_pdf_image/<filename>", methods=["POST"])
def generate_pdf_image(filename):
    filename = secure_filename(filename)
    src_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.isfile(src_path) or not filename.lower().endswith(".pdf"):
        output = "PDF not found"
    else:
        tempdir = tempfile.mkdtemp(prefix="pdfimg_")
        out_prefix = os.path.join(tempdir, f"{filename}_page")
        command = ["pdftocairo", "-jpeg", src_path, out_prefix]
        try:
            proc = subprocess.run(
                command,
                check=True,
                capture_output=True,
                universal_newlines=True,
                timeout=120,
            )
            images = sorted(
                f
                for f in os.listdir(tempdir)
                if f.endswith(".jpg") or f.endswith(".jpeg")
            )
            if images:
                img_html = "".join(
                    f'<div style="margin:14px 0;"><a href="/pdf_imagefile/{os.path.basename(tempdir)}/{img}" target="_blank">{img}</a><br>'
                    f'<img src="/pdf_imagefile/{os.path.basename(tempdir)}/{img}" width="350"></div>'
                    for img in images
                )
                output = (
                    f"pdftocairo output:\n{proc.stdout}\n{proc.stderr or ''}\n"
                    + img_html
                )
            else:
                output = "No images generated."
        except Exception as e:
            output = f"Failed to generate images: {e}"
    files = [
        f
        for f in os.listdir(UPLOAD_FOLDER)
        if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))
    ]
    hashes = {f: sha256sum(os.path.join(UPLOAD_FOLDER, f)) for f in files}
    return render_template_string(
        HTML_TEMPLATE,
        files=files,
        output=output,
        hashes=hashes,
        archive=False,
        reports=False,
    )


@app.route("/pdf_imagefile/<folder>/<image>")
def send_pdf_image(folder, image):
    folder = secure_filename(folder)
    image = secure_filename(image)
    temp_base = "/tmp"
    dir_path = os.path.join(temp_base, folder)
    return send_from_directory(dir_path, image)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
