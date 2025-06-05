from flask import Blueprint, render_template, session, redirect, url_for, flash, abort
from models.produto import Produto
from models.pedido import Pedido
from models.item_pedido import ItemPedido
from flask_login import login_required, current_user
from models import db
from utils.decorators import admin_required

loja = Blueprint('loja', __name__)

@loja.route('/')
def index():
    produtos = Produto.query.all()
    return render_template('index.html', produtos=produtos)

@loja.route('/produto/<int:id>')
def produto_detalhe(id):
    produto = Produto.query.get_or_404(id)
    return render_template('produto_detalhe.html', produto=produto)

@loja.route('/finalizar-compra')
@login_required
def finalizar_compra():
    carrinho = session.get('carrinho', {})

    if not carrinho:
        flash("Seu carrinho está vazio.")
        return redirect(url_for('carrinho.ver_carrinho'))

    total = 0
    for produto_id, quantidade in carrinho.items():
        produto = Produto.query.get(int(produto_id))
        total += produto.preco * quantidade

    novo_pedido = Pedido(usuario_id=current_user.id, total=total)
    db.session.add(novo_pedido)
    db.session.commit()

    for produto_id, quantidade in carrinho.items():
        item_pedido = ItemPedido(
            pedido_id=novo_pedido.id,
            produto_id=int(produto_id),
            quantidade=quantidade
        )
        db.session.add(item_pedido)

    db.session.commit()

    session['carrinho'] = {}
    flash("Compra finalizada com sucesso.")
    return redirect(url_for('loja.index'))

@loja.route('/meus-pedidos')
@login_required
def meus_pedidos():
    pedidos = Pedido.query.filter_by(usuario_id=current_user.id).order_by(Pedido.data.desc()).all()
    return render_template('meus_pedidos.html', pedidos=pedidos)

