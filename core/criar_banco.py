from .app import create_app
from core.utils.extensions import db
from .models.atendimento import Atendimento
from .models.endereco import Endereco
from .models.paciente import Paciente
from .models.pessoa import Pessoa
from .models.procedimento import Procedimento
from .models.organizacao import Organizacao
from .models.usuario import Usuario
from .models.acesso import Acesso

app = create_app()

with app.app_context():
    db.create_all()
    print("Banco de dados criado com sucesso!")
    print(app.config["SQLALCHEMY_DATABASE_URI"])