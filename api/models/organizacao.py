from api.utils.extensions import db
from datetime import datetime

class Organizacao(db.Model):
    __tablename__ = 'organizacao'

    id_organizacao = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo = db.Column(db.String(6), unique=True, nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    
