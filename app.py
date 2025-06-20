from flask import Flask, render_template, request, redirect, send_file, url_for
import os
import pandas as pd
from werkzeug.utils import secure_filename
from datetime import datetime
from utils.detector import detect_dataset_type
from utils.general_dashboard import generate_dashboard

app = Flask(__name__)

# Create folders for file handling
UPLOAD_FOLDER = "uploads"
DASHBOARD_FOLDER = "downloads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(DASHBOARD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DASHBOARD_FOLDER'] = DASHBOARD_FOLDER

# Allowed extensions
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Homepage - serve HTML
@app.route("/")
def index():
    return render_template("index.html")

# Upload route
@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    if file.filename == '':
        return "No file selected", 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)

        # Detect dataset type (optional logging)
        dataset_type = detect_dataset_type(upload_path)
        print(f"Detected dataset type: {dataset_type}")

        # Generate dashboard
        dashboard_filename = filename.rsplit('.', 1)[0] + "_dashboard.xlsx"
        dashboard_path = os.path.join(app.config['DASHBOARD_FOLDER'], dashboard_filename)
        success = generate_dashboard(upload_path, dashboard_path)

        if success:
            return "Success", 200
        else:
            return "Processing failed", 500

    return "Invalid file format", 400

# Download route
@app.route("/download")
def download_file():
    files = os.listdir(DASHBOARD_FOLDER)
    if not files:
        return "No dashboard available", 404
    latest_file = max([os.path.join(DASHBOARD_FOLDER, f) for f in files], key=os.path.getctime)
    return send_file(latest_file, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
