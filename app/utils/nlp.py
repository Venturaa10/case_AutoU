import pdfplumber
import google.generativeai as genai
import logging
import json
import os
from dotenv import load_dotenv
import re

logger = logging.getLogger(__name__)
load_dotenv()

# configurar API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


models = genai.list_models()
for m in models:
    print(m.name)


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
# 2. CLASSIFICAÇÃO + RESPOSTA (Gemini)
# ---------------------------
def classify_and_reply(text):
    prompt = f"""
    Analise o email abaixo e retorne APENAS um JSON válido.

    Email: \"\"\"{text}\"\"\"

    Tarefas:
    1. Classificar como: "Produtivo" ou "Improdutivo".
    2. Criar uma resposta automática adequada:
       - Se for produtivo → resposta objetiva e profissional.
       - Se for improdutivo → resposta leve e cordial.

    Formato obrigatório:
    {{
        "categoria": "",
        "resposta": ""
    }}
    """

    model = genai.GenerativeModel("gemini-flash-latest")
    response = model.generate_content(prompt)

    # Tentar extrair JSON de qualquer lugar do texto retornado
    text_output = response.text
    json_match = re.search(r"\{.*\}", text_output, re.DOTALL)

    if json_match:
        try:
            data = json.loads(json_match.group())
            return data
        except Exception as e:
            logger.error(f"Erro ao converter JSON: {e}")
    else:
        logger.error("Nenhum JSON encontrado na resposta do Gemini")

    return {
        "categoria": "Indefinido",
        "resposta": "Não foi possível gerar resposta automática."
    }