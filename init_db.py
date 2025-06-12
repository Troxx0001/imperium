from app import app, db
from models.admin_log import AdminLog
from models.item_pedido import ItemPedido
from models.pedido import Pedido
from models.produto import Produto
from models.usuario import Usuario

with app.app_context():
    db.create_all()
    print("Tabelas criadas com sucesso.")
