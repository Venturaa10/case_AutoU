import pdfplumber
from transformers import pipeline
from .preprocess import preprocess_text
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


def classify_text(text):
    # Pré-processamento REAL (stopwords, lematização etc.)
    processed_text = preprocess_text(text)

    # Labels do modelo zero-shot
    labels = [
        "É um pedido de tarefa ou solicitação de trabalho",
        "É apenas uma conversa informal, sem solicitação de tarefa"
    ]

    # Classificação (usando o texto pré-processado)
    result = classifier(processed_text, candidate_labels=labels)

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
def generate_reply(text, category):
    generator = pipeline(
        "text-generation",
        model="Qwen/Qwen2.5-1.5B-Instruct",
        device_map="auto",
        max_new_tokens=100,
        temperature=0.2,
        top_p=0.9
    )

    if category == "Produtivo":
        tone = "direto e profissional"
    elif category == "Improdutivo":
        tone = "leve e cordial"
    else:
        tone = "neutro e educado"

    prompt = f"""
Responda ao e-mail abaixo de forma {tone}.
Não repita o texto original. Apenas escreva a resposta final, curta e objetiva.

Email:
{text}

Resposta:
"""

    output = generator(prompt)[0]["generated_text"]

    # remove tudo antes de "Resposta:" caso o modelo repita
    if "Resposta:" in output:
        output = output.split("Resposta:")[-1].strip()

    return output
