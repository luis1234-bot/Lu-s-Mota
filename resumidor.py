from transformers import pipeline

# Carrega o modelo de resumo (pode demorar na primeira execução)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

texto_longo = """
Aqui vai o texto que você quer resumir. Por exemplo, a transcrição de um vídeo do YouTube.
Quanto mais longo o texto, melhor o resumo. O modelo BART é ótimo para resumir artigos, vídeos, etc.
"""

# Gera o resumo
resumo = summarizer(texto_longo, max_length=130, min_length=30, do_sample=False)

print("📌 Resumo:")
print(resumo[0]['summary_text'])