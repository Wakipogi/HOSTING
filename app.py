from flask import Flask, render_template, request, jsonify
import os
import subprocess
import threading

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Use Render's PORT environment variable
PORT = int(os.getenv("PORT", 5000))  

# Store running processes and logs
running_processes = {}
log_storage = {}

@app.route("/")
def home():
    python_files = os.listdir(UPLOAD_FOLDER)
    return render_template("index.html", files=python_files)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files["file"]
    if file.filename == "" or not file.filename.endswith(".py"):
        return jsonify({"error": "Invalid file type. Please upload a Python file."})

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    return jsonify({"message": f"{file.filename} uploaded!", "filename": file.filename})

@app.route("/start/<script_name>")
def start_script(script_name):
    script_path = os.path.join(UPLOAD_FOLDER, script_name)

    if script_name in running_processes:
        return jsonify({"error": f"{script_name} is already running."})

    process = subprocess.Popen(
        ["python3", script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    running_processes[script_name] = process
    log_storage[script_name] = []

    def capture_output():
        for line in iter(process.stdout.readline, ""):
            log_storage[script_name].append(line.strip())

    threading.Thread(target=capture_output, daemon=True).start()

    return jsonify({"message": f"{script_name} started!"})

@app.route("/stop/<script_name>")
def stop_script(script_name):
    if script_name in running_processes:
        running_processes[script_name].terminate()
        running_processes.pop(script_name, None)
        return jsonify({"message": f"{script_name} stopped!"})
    return jsonify({"error": f"{script_name} is not running."})

@app.route("/logs/<script_name>")
def get_logs(script_name):
    logs = log_storage.get(script_name, ["No output yet."])
    return jsonify({"logs": "\n".join(logs)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
