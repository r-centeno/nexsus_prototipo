from flask import Flask
from flask_cors import CORS
from api.utils.extensions import db, migrate
from api.config import Config
from api.routes.registro import registro_bp
from api.routes.auth import auth_bp 
# from api.routes.login import login_bp 
from api.routes.dashboard import dashboard_bp 

def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    app.register_blueprint(registro_bp)
    app.register_blueprint(auth_bp)
    # app.register_blueprint(login_bp)
    app.register_blueprint(dashboard_bp)

    @app.route('/')
    def home():
        return {"status": "API Online", "version": "1.0"}

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)