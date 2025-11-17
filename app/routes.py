from flask import Blueprint, render_template, request
from app.utils.nlp import extract_text_from_file, classify_and_reply

bp = Blueprint("main", __name__)

@bp.route("/", methods=["GET"])
def index():
    """
    Rota da página inicial.

    Renderiza o formulário de envio de email para classificação e geração
    de resposta automática.

    Método: GET
    URL: /
    Template: index.html
    """
    return render_template("index.html")


@bp.route("/process", methods=["POST"])
def process_email():
    """
    Rota de processamento de email.

    Recebe o texto do email via formulário (textarea) ou arquivo (.txt/.pdf).
    Utiliza a função `classify_and_reply` para classificar o email como
    "Produtivo" ou "Improdutivo" e gerar uma resposta automática
    adequada à categoria.

    Se nenhum texto ou arquivo for enviado, retorna a página inicial
    com uma mensagem de erro.

    Método: POST
    URL: /process
    Template: result.html
    """

    # Texto enviado manualmente
    text = request.form.get("email_text", "").strip()

    # Se o texto não veio, tenta arquivo
    if not text:
        file = request.files.get("file")
        if file and file.filename.strip():
            text = extract_text_from_file(file)

    # Se não houver texto também, retorna mensagem de erro ao usuario. 
    if not text:
        return render_template("index.html", error="Por favor, envie um arquivo ou cole o texto.")

    # Nova função única (Gemini)
    result = classify_and_reply(text)

    # Extrai categoria e sugestão do resultado
    category = result.get("categoria", "Indefinido")
    suggestion = result.get("resposta", "Não foi possível gerar resposta.")

    return render_template(
        "result.html",
        text=text,
        category=category,
        suggestion=suggestion
    )


# @bp.route("/process_json", methods=["POST"])
# def process_email_json():
#     text = request.form.get("email_text", "").strip()
#     if not text:
#         file = request.files.get("file")
#         if file and file.filename.strip():
#             text = extract_text_from_file(file)

#     if not text:
#         return {"error": "Nenhum texto enviado"}, 400

#     result = classify_and_reply(text)
#     return result  # já é um dict com categoria e resposta
