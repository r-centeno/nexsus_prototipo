from api.utils.extensions import db

class Endereco(db.Model):
    __tablename__ = 'endereco'

    id_endereco = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_pessoa = db.Column(db.Integer, db.ForeignKey('pessoa.id_pessoa'), nullable=False)
    cep = db.Column(db.String(8))
    tipo_logradouro = db.Column(db.String(3))    
    nome_logradouro = db.Column(db.String(100))
    numero = db.Column(db.String(20))
    complemento = db.Column(db.String(50))  
    bairro = db.Column(db.String(100))
    cidade = db.Column(db.String(100))
    uf = db.Column(db.String(2))
    ibge = db.Column(db.String(6))           

    pessoa = db.relationship('Pessoa', back_populates='endereco')