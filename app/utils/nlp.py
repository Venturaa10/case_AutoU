import pdfplumber
from transformers import pipeline
import logging
logger = logging.getLogger(__name__)
import re

# ---------------------------
# 1. EXTRAÇÃO DE TEXTO
# ---------------------------

def extract_text_from_file(file):
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        pdf = pdfplumber.open(file)
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"
        return text

    if filename.endswith(".txt"):
        return file.read().decode("utf-8")

    return ""


# ---------------------------
# 2. CLASSIFICAÇÃO (HuggingFace)
# ---------------------------

classifier = pipeline("zero-shot-classification",
                      model="facebook/bart-large-mnli")


def clean_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def classify_text(text):
    text_clean = clean_text(text)
    
    labels = [
        "É um pedido de tarefa ou solicitação de trabalho",
        "É apenas uma conversa informal, sem solicitação de tarefa"
    ]

    result = classifier(text_clean, candidate_labels=labels)

    logger.debug(f"{result}")

    scores = result["scores"]
    diff = abs(scores[0] - scores[1])

    if diff < 0.25:
        return "Neutro"

    chosen = result["labels"][0]

    if "tarefa" in chosen or "solicitação" in chosen:
        return "Produtivo"
    else:
        return "Improdutivo"


# ---------------------------
# 3. GERAR RESPOSTA AUTOMÁTICA (HuggingFace)
# ---------------------------

generator = pipeline("text2text-generation",
                     model="google/flan-t5-base")

def generate_reply(text, category):
    prompt = f"""
Você é um assistente que responde emails de forma objetiva, educada e profissional.
Sempre responda em português do Brasil.
Não repita o texto original. Não explique nada. Apenas gere a resposta final.

Aqui estão alguns exemplos de boa resposta:

[Exemplo 1 — Pedido Produtivo]
Email original:
"Você pode enviar o relatório atualizado ainda hoje?"
Resposta:
"Claro! Vou gerar e enviar o relatório atualizado ainda hoje."

[Exemplo 2 — Produtivo]
Email original:
"Preciso que gere os boletos do mês passado."
Resposta:
"Sem problemas, vou gerar os boletos do mês passado e te envio em seguida."

[Exemplo 3 — Improdutivo]
Email original:
"Bom dia! Tudo bem? Como foi seu final de semana?"
Resposta:
"Bom dia! Tudo ótimo por aqui, e você? :)"

Agora responda o email abaixo:

Categoria: {category}

Email:
\"\"\"{text}\"\"\"

Resposta:
"""

    result = generator(prompt, max_length=200)
    return result[0]["generated_text"].strip()