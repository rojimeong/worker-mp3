
from flask import Flask, request, jsonify, send_file
import os
import yt_dlp
import uuid

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "YouTube MP3 Downloader Worker Aktif ✅"

@app.route("/download", methods=["POST"])
def download_mp3():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL tidak ditemukan."}), 400

    try:
        filename = f"music_{uuid.uuid4().hex}.mp3"
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'/tmp/{filename}',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(f"/tmp/{filename}", as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
