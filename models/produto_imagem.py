from models import db

class ProdutoImagem(db.Model):
    __tablename__ = 'produto_imagem'
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id', ondelete='CASCADE'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)  
    ordem = db.Column(db.Integer, nullable=False, default=0)
