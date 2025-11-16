from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from utils.extensions import db
from routes.registro import registro_bp
#from routes.dashboard import dashboard_bp
from routes.auth import auth_bp
from routes.login import login_bp
from models.procedimento import Procedimento
from models.atendimento import Atendimento
from models.paciente import Paciente
from models.pessoa import Pessoa
from models.endereco import Endereco
from models.organizacao import Organizacao
from models.acesso import Acesso
from models.usuario import Usuario

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)
    #CORS(app)
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Erro interno no servidor"}), 500

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Rota não encontrada"}), 404

    app.register_blueprint(registro_bp)
    app.register_blueprint(auth_bp)
    #app.register_blueprint(dashboard_bp)
    app.register_blueprint(login_bp)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5051)



