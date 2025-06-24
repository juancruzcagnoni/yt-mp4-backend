from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from utils import download_youtube_video
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/convert', methods=['POST'])
def convert():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        filename = download_youtube_video(url)
        return jsonify({'file': filename})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/downloads/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory('downloads', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
