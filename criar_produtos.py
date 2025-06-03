from app import app, db
from models.produto import Produto

with app.app_context():
    # Criando produtos
    p1 = Produto(
        nome="Mouse Gamer RGB",
        marca="Redragon",
        descricao="Mouse gamer com sensor óptico de alta precisão e iluminação RGB.",
        preco=149.90,
        estoque=20,
        imagem="https://via.placeholder.com/200x200?text=Mouse+Gamer"
    )

    p2 = Produto(
        nome="Teclado Mecânico",
        marca="HyperX",
        descricao="Teclado mecânico com switches vermelhos, ideal para jogos.",
        preco=299.90,
        estoque=15,
        imagem="https://via.placeholder.com/200x200?text=Teclado"
    )

    # Inserindo no banco
    db.session.add_all([p1, p2])
    db.session.commit()
    print("Produtos adicionados com sucesso.")
