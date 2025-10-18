from models import db

class Produto(db.Model):
    __tablename__ = 'produto'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False)
    imagem = db.Column(db.String(255))  
    ativo = db.Column(db.Boolean, nullable=False, server_default=db.text('true'))
    
    imagens = db.relationship(
        'ProdutoImagem',
        backref='produto',
        cascade='all, delete-orphan',
        passive_deletes=True,
        order_by='ProdutoImagem.ordem',
        lazy='selectin',
    )
