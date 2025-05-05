import textrazor

# Defina sua chave diretamente aqui (só para testes)
textrazor.api_key = "3af92e4bd1aaf18bf95deec11af9d01968b3f24c33f7ef2846cc58d3"  # substitua pela chave real

def summarize_text(text):
    client = textrazor.TextRazor(extractors=["entities", "topics", "summary"])
    response = client.analyze(text)

    if response.ok:
        # Usa o resumo gerado pela API (experimental)
        try:
            summaries = response.response.summary
            if summaries:
                return summaries[0]
            else:
                return "Não foi possível gerar um resumo."
        except AttributeError:
            return "Resumo não disponível na resposta."
    else:
        raise Exception(f"Erro TextRazor: {response.status} - {response.json}")