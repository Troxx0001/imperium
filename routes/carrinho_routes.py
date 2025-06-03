from flask import Blueprint, session, redirect, url_for, render_template, flash, request
from models.produto import Produto

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

@carrinho_bp.route('/finalizar_compra')
def finalizar_compra():
    session.pop('carrinho', None)
    return "<h2>Compra finalizada com sucesso! Obrigado por comprar conosco.</h2>"

@carrinho_bp.route('/remover_do_carrinho', methods=['POST'])
def remover_do_carrinho():
    produto_id = str(request.form['produto_id'])
    if 'carrinho' in session and produto_id in session['carrinho']:
        session['carrinho'].pop(produto_id)
        flash('Produto removido do carrinho.', 'info')
    else:
        flash('Produto não encontrado no carrinho.', 'warning')
    return redirect(url_for('carrinho.ver_carrinho'))
