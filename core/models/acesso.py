from core.utils.extensions import db
from datetime import datetime

class Acesso(db.Model):
    __tablename__ = 'acesso'

    id_acesso = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Relacionamento com Usuario
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    usuario = db.relationship('Usuario', backref=db.backref('acessos', lazy=True))

    # Relacionamento com Pessoa
    id_pessoa = db.Column(db.Integer, db.ForeignKey('pessoa.id_pessoa'), nullable=False)
    pessoa = db.relationship('Pessoa', backref=db.backref('acessos', lazy=True))

    email = db.Column(db.String(120), nullable=False)
    codigo = db.Column(db.String(6), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    validado = db.Column(db.Boolean, default=False)

    ip = db.Column(db.String(45))  # IPv4 ou IPv6
    localizacao = db.Column(db.String(120))  # Cidade, país ou coordenadas
