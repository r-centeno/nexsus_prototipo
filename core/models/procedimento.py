from core.utils.extensions import db
from datetime import datetime

class Procedimento(db.Model):
    __tablename__ = 'procedimento'

    id_procedimento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cod_procedimento = db.Column(db.String(10), unique=True, nullable=False)
    nome_procedimento = db.Column(db.String(120), nullable=False)
    vlr_procedimento = db.Column(db.Numeric(10, 2), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    
    atendimentos = db.relationship('Atendimento', back_populates='procedimento', lazy=True)

