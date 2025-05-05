from transformers import pipeline

# Carrega o modelo localmente (é baixado na primeira vez)
summarizer = pipeline("summarization", model="csebuetnlp/mT5_multilingual_XLSum")

def summarize_text(text):
    resumo = summarizer(text, max_length=150, min_length=30, do_sample=False)
    return resumo[0]["summary_text"]