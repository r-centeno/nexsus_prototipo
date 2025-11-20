from flask import Flask
from flask_cors import CORS
from api.utils.extensions import db, migrate
from api.config import Config
from api.routes.registro import registro_bp
from api.routes.auth import auth_bp 
# from api.routes.login import login_bp     # Exemplo: descomente se já estiver implementado
from api.routes.dashboard import dashboard_bp 

def create_app():
    app = Flask(__name__)
    
    # Carrega as configurações (definidas em api/config.py)
    app.config.from_object(Config)

    # Inicializa as extensões
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Habilita CORS (Cross-Origin Resource Sharing)
    # Isso é vital para o frontend acessar o backend no Vercel
    # 'resources={r"/api/*": ...}' restringe o CORS apenas às rotas da API
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Registro das Blueprints
    app.register_blueprint(registro_bp)
    app.register_blueprint(auth_bp)
    # app.register_blueprint(login_bp)
    app.register_blueprint(dashboard_bp)

    # Rota de verificação de saúde (opcional, mas útil para debug no Vercel)
    @app.route('/')
    def home():
        return {"status": "API Online", "version": "1.0"}

    return app

# Instância da aplicação para execução local
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)