import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import download_youtube_video  # asumimos que lo tenés

app = Flask(__name__)
CORS(app)


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


@app.route("/")
def home():
    return jsonify({"status": "🟢 API working"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # Detect if running in Render
    is_render = os.environ.get("RENDER", False)

    host = "0.0.0.0" if is_render else "127.0.0.1"
    app.run(debug=not is_render, host=host, port=port)
