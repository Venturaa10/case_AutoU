import re
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)
nltk.download("stopwords", quiet=True)

nlp = spacy.load("pt_core_news_sm")
STOPWORDS = set(stopwords.words("portuguese"))

def preprocess_text(text: str) -> str:
    """
    Pré-processa o texto de um email para NLP.

    Importante para melhorar a qualidade e analise do texto pelo modelo da IA.

    Passos realizados:
    1. Converte para minúsculas e remove caracteres indesejados.
    2. Tokeniza o texto em palavras.
    3. Remove stopwords e tokens muito curtos.
    4. Lematiza os tokens restantes usando spaCy.

    Args:
        text (str): Texto original do email.

    Returns:
        str: Texto processado, pronto para análise ou classificação.

    Exemplo:
        >>> preprocess_text("Olá! Preciso de ajuda com meu sistema.")
        'precisar ajuda sistema'
    """

    # lowercase + limpeza básica
    text = text.lower()
    text = re.sub(r"[^a-záéíóúâêôãõç0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    # tokenização, pega o texto inteiro e separa em palavras individuais.
    tokens = word_tokenize(text, language="portuguese")

    # remover stopwords e tokens curtos. Tokens muito curtos removidos para facilitar a leitura do modelo.
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 2]

    # lematização
    doc = nlp(" ".join(tokens))
    lemmas = [token.lemma_ for token in doc]

    return " ".join(lemmas)
