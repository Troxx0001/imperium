from models import db

class Produto(db.Model):
    __tablename__ = 'produto'

    # elementos da tabela
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False)
    imagem = db.Column(db.String(255))  # URL/caminho ou apenas filename
    ativo = db.Column(db.Boolean, nullable=False, default=True, server_default=db.text('true'))

    def __repr__(self):
        return f"<Produto {self.id} {self.nome} ativo={self.ativo}>"
