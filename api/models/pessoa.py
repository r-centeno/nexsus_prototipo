from api.utils.extensions import db
from datetime import datetime


class Pessoa(db.Model):
    __tablename__ = 'pessoa'

    id_pessoa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    dt_nascimento = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.String(1))
    raca = db.Column(db.String(2))
    nacionalidade = db.Column(db.String(3))
    cns = db.Column(db.String(15))
    ddd = db.Column(db.String(2))
    telefone = db.Column(db.String(10))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)


    paciente = db.relationship('Paciente', back_populates='pessoa', uselist=False, cascade='all, delete-orphan')
    endereco = db.relationship('Endereco', back_populates='pessoa', lazy=True, cascade='all, delete-orphan')
    atendimentos = db.relationship('Atendimento', back_populates='pessoa', lazy=True, cascade='all, delete-orphan')
