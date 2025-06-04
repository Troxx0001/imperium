from flask import Flask
from config import Config
from models import db
from models.produto import Produto
from models.usuario import Usuario
from models.pedido import Pedido
from models.item_pedido import ItemPedido

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.session.query(ItemPedido).delete()
    db.session.query(Pedido).delete()
    db.session.query(Produto).delete()
    db.session.query(Usuario).filter(Usuario.admin == False).delete()
    db.session.commit()
    print("Banco de dados limpo com sucesso (exceto usuários admin).")

