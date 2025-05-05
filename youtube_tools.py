from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
import re
from typing import Optional

# Configurações otimizadas para o Render (plano gratuito)
MODEL_NAME = "sshleifer/distilbart-cnn-6-6"  # Modelo leve (6 camadas)
MAX_INPUT_LENGTH = 512  # Reduzido para economizar memória
SUMMARY_LENGTH = 100
MIN_LENGTH = 30

# Cache global do modelo (carregado apenas quando necessário)
_summarizer = None

def extract_video_id(video_url: str) -> Optional[str]:
    """Extrai o ID do vídeo de forma otimizada."""
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", video_url)
    return match.group(1) if match else None

def get_summarizer():
    """Carrega o modelo apenas quando necessário com configurações leves."""
    global _summarizer
    if _summarizer is None:
        _summarizer = pipeline(
            "summarization",
            model=MODEL_NAME,
            device=-1,  # Força uso de CPU
            framework="pt"
        )
    return _summarizer

def summarize_youtube_video(video_url: str) -> str:
    """Versão ultra-otimizada para o Render free tier."""
    try:
        # 1. Validação rápida
        video_id = extract_video_id(video_url)
        if not video_id:
            return "URL inválida"
        
        # 2. Obtém apenas os primeiros 60 segmentos (30-60s de vídeo)
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=['pt'],
            preserve_formatting=False
        )[:60]
        
        if not transcript:
            return "Transcrição não disponível"
        
        # 3. Texto compactado (remove espaços extras)
        text = " ".join(t['text'].strip() for t in transcript)
        text = " ".join(text.split())[:MAX_INPUT_LENGTH]  # Corte seguro
        
        # 4. Sumarização minimalista
        summarizer = get_summarizer()
        summary = summarizer(
            text,
            max_length=SUMMARY_LENGTH,
            min_length=MIN_LENGTH,
            do_sample=False,
            truncation=True
        )
        
        return summary[0]['summary_text'].strip()
    
    except Exception as e:
        return f"Erro: {str(e)}"