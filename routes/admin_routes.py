from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

from models import db
from models.produto import Produto
from models.pedido import Pedido
from models.usuario import Usuario
from models.admin_log import AdminLog
from forms import ProductForm, OrderFilterForm, AdminLoginForm

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def log_action(acao):
    if current_user.is_authenticated and current_user.admin:
        log = AdminLog(usuario_id=current_user.id, acao=acao)
        db.session.add(log)
        db.session.commit()


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data, admin=True).first()
        if user and check_password_hash(user.senha, form.senha.data):
            login_user(user)
            flash('Login de administrador realizado com sucesso!', 'success')
            return redirect(url_for('admin.dashboard'))
        flash('Credenciais inválidas ou usuário não é administrador.', 'danger')
    return render_template('admin/login.html', form=form)


@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado.', 'info')
    return redirect(url_for('admin.login'))


@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.admin:
        return redirect(url_for('loja.index'))
    total_produtos = Produto.query.count()
    total_usuarios = Usuario.query.count()
    total_pedidos = Pedido.query.count()
    return render_template('admin/dashboard.html',
                           total_produtos=total_produtos,
                           total_usuarios=total_usuarios,
                           total_pedidos=total_pedidos)


@admin_bp.route('/produtos')
@login_required
def produtos():
    if not current_user.admin:
        return redirect(url_for('loja.index'))
    produtos = Produto.query.all()
    return render_template('admin/produtos/lista.html', produtos=produtos)


@admin_bp.route('/produtos/novo', methods=['GET', 'POST'])
@login_required
def produto_novo():
    if not current_user.admin:
        return redirect(url_for('loja.index'))
    form = ProductForm()
    if form.validate_on_submit():
        produto = Produto(nome=form.nome.data,
                          marca=form.marca.data,
                          descricao=form.descricao.data,
                          preco=form.preco.data,
                          estoque=form.estoque.data,
                          imagem=form.imagem.data)
        db.session.add(produto)
        db.session.commit()
        log_action(f'Adicionou produto {produto.nome}')
        flash('Produto adicionado com sucesso.', 'success')
        return redirect(url_for('admin.produtos'))
    return render_template('admin/produtos/form.html', form=form)


@admin_bp.route('/produtos/<int:produto_id>/editar', methods=['GET', 'POST'])
@login_required
def produto_editar(produto_id):
    if not current_user.admin:
        return redirect(url_for('loja.index'))
    produto = Produto.query.get_or_404(produto_id)
    form = ProductForm(obj=produto)
    if form.validate_on_submit():
        form.populate_obj(produto)
        db.session.commit()
        log_action(f'Editou produto {produto.nome}')
        flash('Produto atualizado.', 'success')
        return redirect(url_for('admin.produtos'))
    return render_template('admin/produtos/form.html', form=form, produto=produto)


@admin_bp.route('/produtos/<int:produto_id>/excluir', methods=['POST'])
@login_required
def produto_excluir(produto_id):
    if not current_user.admin:
        return redirect(url_for('loja.index'))
    produto = Produto.query.get_or_404(produto_id)
    db.session.delete(produto)
    db.session.commit()
    log_action(f'Excluiu produto {produto.nome}')
    flash('Produto excluído.', 'info')
    return redirect(url_for('admin.produtos'))


@admin_bp.route('/pedidos', methods=['GET', 'POST'])
@login_required
def pedidos():
    if not current_user.admin:
        return redirect(url_for('loja.index'))
    form = OrderFilterForm()
    query = Pedido.query
    if form.validate_on_submit() and form.status.data != 'todos':
        query = query.filter_by(status=form.status.data)
    pedidos = query.order_by(Pedido.data.desc()).all()
    return render_template('admin/pedidos/lista.html', pedidos=pedidos, form=form)


@admin_bp.route('/pedidos/<int:pedido_id>')
@login_required
def pedido_detalhe(pedido_id):
    if not current_user.admin:
        return redirect(url_for('loja.index'))
    pedido = Pedido.query.get_or_404(pedido_id)
    return render_template('admin/pedidos/detalhe.html', pedido=pedido)


@admin_bp.route('/usuarios')
@login_required
def usuarios():
    if not current_user.admin:
        return redirect(url_for('loja.index'))
    usuarios = Usuario.query.all()
    return render_template('admin/usuarios/lista.html', usuarios=usuarios)


@admin_bp.route('/usuarios/<int:usuario_id>/promover', methods=['POST'])
@login_required
def usuario_promover(usuario_id):
    if not current_user.admin:
        return redirect(url_for('loja.index'))
    usuario = Usuario.query.get_or_404(usuario_id)
    usuario.admin = not usuario.admin
    db.session.commit()
    log_action(f'Alterou privilégio de {usuario.nome}')
    return redirect(url_for('admin.usuarios'))


@admin_bp.route('/usuarios/<int:usuario_id>/desativar', methods=['POST'])
@login_required
def usuario_desativar(usuario_id):
    if not current_user.admin:
        return redirect(url_for('loja.index'))
    usuario = Usuario.query.get_or_404(usuario_id)
    usuario.ativo = not usuario.ativo
    db.session.commit()
    log_action(f'Alterou status de {usuario.nome}')
    return redirect(url_for('admin.usuarios'))


@admin_bp.route('/logs')
@login_required
def logs():
    if not current_user.admin:
        return redirect(url_for('loja.index'))
    logs = AdminLog.query.order_by(AdminLog.data.desc()).all()
    return render_template('admin/logs.html', logs=logs)
