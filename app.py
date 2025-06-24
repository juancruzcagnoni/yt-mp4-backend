import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from utils import download_youtube_video

app = Flask(__name__)
CORS(app)

# Detectar si estamos en Render o local
IS_RENDER = os.environ.get("RENDER") is not None
BASE_DOWNLOAD_DIR = "/tmp/downloads" if IS_RENDER else os.path.join(os.path.dirname(__file__), "downloads")

@app.route("/api/convert", methods=["POST"])
def convert():
    data = request.get_json()
    url = data.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        filename = download_youtube_video(url)
        return jsonify({"file": filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/downloads/<filename>")
def serve_file(filename):
    try:
        return send_from_directory(BASE_DOWNLOAD_DIR, filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": f"Download error: {str(e)}"}), 404


@app.route("/")
def home():
    return jsonify({"status": "🟢 API working"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    host = "0.0.0.0" if IS_RENDER else "127.0.0.1"
    app.run(debug=not IS_RENDER, host=host, port=port)
