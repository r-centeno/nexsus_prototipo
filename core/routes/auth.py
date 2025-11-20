from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from core.models.usuario import Usuario
from core.models.pessoa import Pessoa
from core.models.acesso import Acesso
from core.utils.extensions import db
from email.message import EmailMessage
import smtplib, random, os
from datetime import datetime
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/api/login", methods=["POST", "OPTIONS"])
@cross_origin()
def login():
    dados = request.get_json()
    username = dados.get("username")
    senha = dados.get("senha")

    if not username or not senha:
        return jsonify({"erro": "Usuário e senha são obrigatórios"}), 400

    usuario = Usuario.query.filter_by(username=username).first()
    if not usuario or not usuario.verificar_senha(senha):
        return jsonify({"erro": "Credenciais inválidas"}), 401

    return jsonify({
        "mensagem": "Login bem-sucedido",
        "usuario": {
            "id": usuario.id_usuario,
            "username": usuario.username,
            "email": usuario.email
        }
    }), 200

@auth_bp.route("/api/enviar-codigo", methods=["POST"])
@cross_origin()
def enviar_codigo():
    dados = request.get_json()
    nome_usuario = dados.get("usuario")

    if not nome_usuario:
        return jsonify({"erro": "Campo 'usuario' é obrigatório"}), 400

    usuario = Usuario.query.filter_by(username=nome_usuario).first()
    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    pessoa = usuario.pessoa
    if not pessoa:
        return jsonify({"erro": "Pessoa vinculada não encontrada"}), 404

    email = usuario.email
    codigo = str(random.randint(100000, 999999))
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)

    try:
        msg = EmailMessage()
        msg["Subject"] = "Código de Verificação - NEXSUS"
        msg["From"] = SMTP_USER
        msg["To"] = email
        msg.set_content(f"Seu código de verificação é: {codigo}")

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SMTP_USER, SMTP_PASS)
            smtp.send_message(msg)
    except Exception as e:
        print("Erro ao enviar e-mail:", e)
        return jsonify({"erro": "Falha ao enviar e-mail"}), 500

    novo_acesso = Acesso(
        id_usuario=usuario.id_usuario,
        id_pessoa=pessoa.id_pessoa,
        email=email,
        codigo=codigo,
        ip=ip,
        criado_em=datetime.utcnow(),
        validado=False
    )
    db.session.add(novo_acesso)
    db.session.commit()

    return jsonify({"mensagem": "Código enviado com sucesso", "email": email}), 200

@auth_bp.route("/api/validar-codigo", methods=["POST"])
@cross_origin()
def validar_codigo():
    dados = request.get_json()
    email = dados.get("email")
    codigo = dados.get("codigo")

    if not email or not codigo:
        return jsonify({"erro": "E-mail e código são obrigatórios"}), 400

    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    acesso = Acesso.query.filter_by(
        id_usuario=usuario.id_usuario,
        email=email,
        codigo=codigo,
        validado=False
    ).order_by(Acesso.criado_em.desc()).first()

    if not acesso:
        return jsonify({"erro": "Código inválido ou expirado"}), 400

    acesso.validado = True
    db.session.commit()

    return jsonify({"mensagem": "Código validado com sucesso"}), 200

@auth_bp.route("/api/redefinir-senha", methods=["POST"])
@cross_origin()
def redefinir_senha():
    dados = request.get_json()
    email = dados.get("email")
    nova_senha = dados.get("novaSenha")

    if not email or not nova_senha:
        return jsonify({"erro": "E-mail e nova senha são obrigatórios"}), 400

    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404

    try:
        senha_criptografada = generate_password_hash(nova_senha)
        usuario.senha_hash = senha_criptografada
        db.session.commit()
        return jsonify({"mensagem": "Senha atualizada com sucesso"}), 200
    except Exception as e:
        db.session.rollback()
        print("Erro ao redefinir senha:", e)
        return jsonify({"erro": "Falha ao atualizar senha"}), 500
