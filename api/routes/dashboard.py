from flask import Blueprint, jsonify
from utils.dashboard_data import obter_dados_dashboard

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('http://127.0.0.1:5051/api/dashboard', methods=['GET'])
def dashboard():
    dados = obter_dados_dashboard()
    return jsonify(dados)

