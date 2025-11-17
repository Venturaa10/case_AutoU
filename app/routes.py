# Contém as rotas:
# página inicial
# upload
# processamento
# exibição do resultado

from flask import Blueprint, render_template, request
from app.utils.nlp import extract_text_from_file, classify_and_reply

bp = Blueprint("main", __name__)

@bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@bp.route("/process", methods=["POST"])
def process_email():
    # Texto enviado manualmente
    text = request.form.get("email_text", "").strip()

    # Se o texto não veio, tenta arquivo
    if not text:
        file = request.files.get("file")
        if file and file.filename.strip():
            text = extract_text_from_file(file)

    if not text:
        return render_template("index.html", error="Por favor, envie um arquivo ou cole o texto.")

    # Nova função única (Gemini)
    result = classify_and_reply(text)

    category = result.get("categoria", "Indefinido")
    suggestion = result.get("resposta", "Não foi possível gerar resposta.")

    return render_template(
        "result.html",
        text=text,
        category=category,
        suggestion=suggestion
    )
