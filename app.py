from flask import Flask, jsonify, send_from_directory
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)
DOWNLOAD_DIR = "downloads"
PLAYLIST_URL = "https://youtube.com/playlist?list=PLxtptE15Su9Gh3ChbP9yxPoVLrxgOCjKG&si=s-voU2leyk8m_BWK"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

def download_playlist():
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'download_archive': 'downloaded.txt',
        'quiet': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([PLAYLIST_URL])

@app.route('/sync', methods=['POST'])
def sync_playlist():
    download_playlist()
    return jsonify({"status": "OK", "message": "Playlist synced"})

@app.route('/list', methods=['GET'])
def list_files():
    files = os.listdir(DOWNLOAD_DIR)
    mp3_files = [f for f in files if f.endswith('.mp3')]
    return jsonify(mp3_files)

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(DOWNLOAD_DIR, filename)

@app.route('/')
@app.route('/status')
def status():
    return jsonify({"status": "online", "message": "Servidor funcionando correctamente"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
