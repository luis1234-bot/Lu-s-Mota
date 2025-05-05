from flask import Flask, render_template, request
from youtube_tools import extract_video_id, summarize_youtube_video

# Primeiro cria a instância do Flask
app = Flask(__name__)

# Depois define as rotas
@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    error = ""
    
    if request.method == "POST":
        url = request.form.get("youtube_url")
        if url:  # Verifica se a URL não está vazia
            try:
                summary = summarize_youtube_video(url)
            except Exception as e:
                error = f"Ocorreu um erro: {str(e)}"
        else:
            error = "Por favor, insira uma URL do YouTube"

    return render_template("index.html", resumo=summary, erro=error)

if __name__ == "__main__":
    app.run(debug=True, port=5000)