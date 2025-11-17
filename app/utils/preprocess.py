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
    # lowercase + limpeza básica
    text = text.lower()
    text = re.sub(r"[^a-záéíóúâêôãõç0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    # tokenização
    tokens = word_tokenize(text, language="portuguese")

    # remover stopwords e tokens curtos
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 2]

    # lematização
    doc = nlp(" ".join(tokens))
    lemmas = [token.lemma_ for token in doc]

    return " ".join(lemmas)
