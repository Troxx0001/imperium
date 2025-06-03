from flask import Blueprint, session, redirect, url_for, render_template, flash, request
from models.produto import Produto
from flask_login import login_required, current_user
from models.pedido import Pedido
from models.item_pedido import ItemPedido
from datetime import datetime
from models import db

carrinho_bp = Blueprint('carrinho', __name__)

@carrinho_bp.route('/adicionar-carrinho/<int:id>')
def adicionar_ao_carrinho(id):
    carrinho = session.get('carrinho', {})
    carrinho[str(id)] = carrinho.get(str(id), 0) + 1
    session['carrinho'] = carrinho
    return redirect(url_for('loja.index'))

@carrinho_bp.route('/carrinho')
def ver_carrinho():
    carrinho = session.get('carrinho', {})
    produtos = []
    total = 0

    for id, qtd in carrinho.items():
        produto = Produto.query.get(int(id))
        subtotal = produto.preco * qtd
        total += subtotal
        produtos.append({
            'produto': produto,
            'quantidade': qtd,
            'subtotal': subtotal
        })

    return render_template('carrinho.html', produtos=produtos, total=total)

@carrinho_bp.route('/finalizar_compra', methods=['POST'])
@login_required
def finalizar_compra():
    carrinho = session.get('carrinho', {})
    if not carrinho:
        flash("Seu carrinho está vazio.", "warning")
        return redirect(url_for('loja.index'))

    # Calcular o total do pedido
    total = 0
    for produto_id, qtd in carrinho.items():
        produto = Produto.query.get(int(produto_id))
        total += produto.preco * int(qtd)

    # Criar o pedido com o total
    pedido = Pedido(usuario_id=current_user.id, data=datetime.now(), total=total)
    db.session.add(pedido)
    db.session.commit()

    # Criar itens do pedido
    for produto_id, qtd in carrinho.items():
        item = ItemPedido(
            pedido_id=pedido.id,
            produto_id=int(produto_id),
            quantidade=int(qtd)
        )
        db.session.add(item)

    db.session.commit()

    # Esvaziar o carrinho
    session.pop('carrinho', None)
    flash("Pedido realizado com sucesso!", "success")
    return redirect(url_for('loja.index'))

@carrinho_bp.route('/remover_do_carrinho', methods=['POST'])
def remover_do_carrinho():
    produto_id = str(request.form['produto_id'])
    if 'carrinho' in session and produto_id in session['carrinho']:
        session['carrinho'].pop(produto_id)
        flash('Produto removido do carrinho.', 'info')
    else:
        flash('Produto não encontrado no carrinho.', 'warning')
    return redirect(url_for('carrinho.ver_carrinho'))
