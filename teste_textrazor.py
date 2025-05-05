import textrazor

# Substitua pela sua chave válida
textrazor.api_key = "3af92e4bd1aaf18bf95deec11af9d01968b3f24c33f7ef2846cc58d3"

client = textrazor.TextRazor(extractors=["entities", "topics", "summary"])

response = client.analyze("O presidente do Brasil visitou a China.")

print("Resumo:", response.summary())