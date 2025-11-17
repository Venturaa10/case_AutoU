import pdfplumber
import google.generativeai as genai
import logging
import json
import os
from dotenv import load_dotenv
import re
from .preprocess import preprocess_text


logger = logging.getLogger(__name__)
load_dotenv()

# configurar API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ---------------------------
# 1. EXTRAÇÃO DE TEXTO
# ---------------------------

def extract_text_from_file(file):
    """
    Extrai o texto de um arquivo enviado (.pdf ou .txt) e aplica pré-processamento NLP.

    Para arquivos PDF:
        - Abre o arquivo usando pdfplumber.
        - Concatena o texto de todas as páginas.

    Para arquivos TXT:
        - Lê o conteúdo como string.

    Em seguida, o texto bruto é pré-processado usando a função `preprocess_text`, 
    que realiza limpeza, tokenização, remoção de stopwords e lematização.

    Args:
        file (werkzeug.datastructures.FileStorage): Arquivo enviado pelo usuário via formulário Flask.

    Returns:
        str: Texto pré-processado pronto para classificação.
             Retorna string vazia se o arquivo não for PDF ou TXT válido.

    Exemplo:
        >>> extract_text_from_file(open("exemplo.pdf", "rb"))
        'preciso ajuda sistema usuário erro'
    """
    
    filename = file.filename.lower()
    text = ""

    # PDF
    if filename.endswith(".pdf"):
        pdf = pdfplumber.open(file)
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    # TXT
    elif filename.endswith(".txt"):
        text = file.read().decode("utf-8")

    # Nenhum formato válido
    else:
        return ""

    # Pré-processamento NLP
    processed_text = preprocess_text(text)
    return processed_text

# ---------------------------
# 2. CLASSIFICAÇÃO + RESPOSTA (Gemini)
# ---------------------------
def classify_and_reply(text):
    """
    Classifica um email como 'Produtivo' ou 'Improdutivo' e gera uma resposta automática usando o modelo Gemini.

    A função envia o texto do email para o modelo de IA, solicitando que retorne um JSON contendo:
        - "categoria": a classificação do email.
        - "resposta": a sugestão de resposta adequada à categoria.

    Caso o modelo não retorne um JSON válido, a função retorna valores padrão indicando falha.

    Args:
        text (str): Texto do email a ser classificado e respondido.

    Returns:
        dict: Um dicionário com as chaves:
            - "categoria" (str): "Produtivo", "Improdutivo" ou "Indefinido".
            - "resposta" (str): Resposta automática gerada ou mensagem de erro.

    Exemplo:
        >>> classify_and_reply("Olá, preciso de ajuda com meu sistema.")
        {'categoria': 'Produtivo', 'resposta': 'Olá, podemos agendar uma sessão para verificar seu sistema.'}
    """

    # Prompt otimizado para Gemini. Especificações das respostas são adicionadas aqui.
    prompt = f"""
    Analise o email abaixo e retorne APENAS um JSON válido.

    IMPORTANTE:
    - NÃO mencione nomes de pessoas na resposta.
    - NÃO personalize a resposta com nomes, mesmo que apareçam no texto original.
    - Sempre responda de forma neutra, como "Olá", "Bom dia", etc.
    - Não inclua assinaturas ou identificações pessoais.

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

    # Modelo Gemini para ler e gerar resposta.
    model = genai.GenerativeModel("gemini-flash-latest")
    response = model.generate_content(prompt)

    # Tentar extrair JSON de qualquer lugar do texto retornado
    text_output = response.text
    json_match = re.search(r"\{.*\}", text_output, re.DOTALL)

    # Busca por JSON.
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