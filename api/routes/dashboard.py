from flask import Blueprint, jsonify
from api.utils.dashboard_data import obter_dados_dashboard

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/api/dashboard", methods=["GET"])
def dashboard():
    dados = obter_dados_dashboard()
    return jsonify(dados)
