from flask import Blueprint, request, jsonify
from api.models import Usuario
from api.utils.extensions import db
from flask_cors import cross_origin

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("http://127.0.0.1:5050/api/login", methods=["POST", "OPTIONS"])
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
