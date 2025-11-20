from core.utils.extensions import db
from datetime import datetime


class Paciente(db.Model):
    __tablename__ = 'paciente'

    id_paciente = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_pessoa = db.Column(db.Integer, db.ForeignKey('pessoa.id_pessoa'), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

    pessoa = db.relationship('Pessoa', back_populates='paciente', lazy=True)
    atendimentos = db.relationship('Atendimento', back_populates='paciente', lazy=True)
