from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import re
from typing import Optional
import torch

# Configurações de otimização
USE_FASTER_MODEL = True  # Alternar para False se quiser maior qualidade
MAX_INPUT_LENGTH = 1024
SUMMARY_LENGTH = 130
MIN_LENGTH = 30
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

def extract_video_id(video_url: str) -> Optional[str]:
    """Extrai o ID do vídeo de forma otimizada."""
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", video_url)
    return match.group(1) if match else None

def initialize_summarizer():
    """Carrega o modelo de sumarização de forma eficiente."""
    if USE_FASTER_MODEL:
        model_name = "sshleifer/distilbart-cnn-12-6"  # Modelo 4x mais rápido
    else:
        model_name = "facebook/bart-large-cnn"
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(DEVICE)
    return pipeline(
        "summarization",
        model=model,
        tokenizer=tokenizer,
        device=0 if DEVICE == "cuda" else -1
    )

# Carrega o modelo uma vez no início (cache)
summarizer = initialize_summarizer()

def summarize_youtube_video(video_url: str) -> str:
    """Versão otimizada para maior velocidade."""
    try:
        # 1. Validação e extração do ID
        if not (video_id := extract_video_id(video_url)):
            return "⚠️ URL inválida"
        
        # 2. Obtém apenas parte da transcrição (primeiros 100 segmentos)
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=['pt', 'en'],
            preserve_formatting=True
        )[:100]  # Limita a 100 segmentos para maior velocidade
        
        if not transcript:
            return "⚠️ Sem transcrição disponível"
        
        # 3. Pré-processamento eficiente
        text = " ".join(t['text'] for t in transcript)
        text = text.replace("\n", " ")[:MAX_INPUT_LENGTH*3]  # Limita o tamanho
        
        # 4. Sumarização em chunks paralelizáveis
        chunks = [
            text[i:i+MAX_INPUT_LENGTH] 
            for i in range(0, min(len(text), MAX_INPUT_LENGTH*3), MAX_INPUT_LENGTH)
        ]
        
        summaries = []
        for chunk in chunks:
            summary = summarizer(
                chunk,
                max_length=SUMMARY_LENGTH,
                min_length=MIN_LENGTH,
                do_sample=False,
                truncation=True
            )
            summaries.append(summary[0]['summary_text'])
        
        return " ".join(summaries).strip()
    
    except Exception as e:
        return f"⚠️ Erro: {str(e)}"

# Exemplo de uso rápido
if __name__ == "__main__":
    import time
    start = time.time()
    
    # Teste com um vídeo curto (opcional)
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    print("Resumo:", summarize_youtube_video(test_url))
    
    print(f"Tempo total: {time.time() - start:.2f} segundos")