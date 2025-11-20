from api.utils.extensions import db
from datetime import datetime

class Atendimento(db.Model):
    __tablename__ = 'atendimento'

    id_atendimento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_pessoa = db.Column(db.Integer, db.ForeignKey('pessoa.id_pessoa'))
    id_paciente = db.Column(db.Integer, db.ForeignKey('paciente.id_paciente'), nullable=False)
    id_procedimento = db.Column(db.Integer, db.ForeignKey('procedimento.id_procedimento'), nullable=False)
    data_procedimento = db.Column(db.Date, nullable=False)
    quantidade = db.Column(db.Integer, default=1)
    cid = db.Column(db.String(4))
    carater_atendimento = db.Column(db.String(2))
    vlr_procedimento = db.Column(db.Numeric(10, 2), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    
    pessoa = db.relationship('Pessoa', back_populates='atendimentos', lazy=True)
    paciente = db.relationship('Paciente', back_populates='atendimentos', lazy=True)
    procedimento = db.relationship('Procedimento', back_populates='atendimentos', lazy=True)



