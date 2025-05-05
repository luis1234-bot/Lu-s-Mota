from flask import Flask, render_template, request
from youtube_tools import extract_video_id, summarize_youtube_video

import os
import resource
resource.setrlimit(resource.RLIMIT_AS, (512 * 1024 * 1024, 512 * 1024 * 1024))  # Limite de 512MB

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    error = ""
    
    if request.method == "POST":
        url = request.form.get("youtube_url")
        if url:
            try:
                summary = summarize_youtube_video(url)
            except Exception as e:
                error = f"Ocorreu um erro: {str(e)}"
        else:
            error = "Por favor, insira uma URL do YouTube"

    return render_template("index.html", resumo=summary, erro=error)

# Remova o app.run() para produção