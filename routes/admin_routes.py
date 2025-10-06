from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app, Response
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from utils.restrito_ip import restrito_por_ip
from models import db
from models.produto import Produto
from models.produto_imagem import ProdutoImagem
from models.pedido import Pedido
from models.usuario import Usuario
from models.admin_log import AdminLog
from forms import ProductForm, OrderFilterForm, AdminLoginForm, IMAGE_EXTENSIONS
from werkzeug.utils import secure_filename
from sqlalchemy import func
import os, io, csv
from datetime import datetime, time
from utils.ipapi_utils import obter_localizacao_por_ip
from uuid import uuid4

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB
MAX_EXTRA_IMAGES = 4
ALLOWED_IMAGE_EXTENSIONS = {ext.lower() for ext in IMAGE_EXTENSIONS}


def _strip(value):
    return value.strip() if value and value.strip() else None


def _is_allowed_extension(filename):
    ext = os.path.splitext(filename.lower())[1].lstrip('.')
    return ext in ALLOWED_IMAGE_EXTENSIONS


def _validate_file_size(file_storage):
    try:
        file_storage.stream.seek(0, os.SEEK_END)
        size = file_storage.stream.tell()
        file_storage.stream.seek(0)
    except Exception:
        size = None
    if size is not None and size > MAX_IMAGE_SIZE:
        raise ValueError('A imagem deve ter até 5 MB.')


def _save_uploaded_image(file_storage):
    filename = secure_filename(file_storage.filename or '')
    if not filename:
        raise ValueError('Nome de arquivo inválido.')
    if not _is_allowed_extension(filename):
        raise ValueError('Formato de imagem não suportado. Use PNG, JPG, JPEG, GIF ou WEBP.')

    _validate_file_size(file_storage)

    ext = os.path.splitext(filename)[1].lower()
    unique_name = f"{uuid4().hex}{ext}"
    upload_dir = os.path.join(current_app.root_path, 'static', 'imagens', 'produtos')
    os.makedirs(upload_dir, exist_ok=True)
    file_storage.save(os.path.join(upload_dir, unique_name))
    return unique_name


def _collect_extra_inputs(form):
    extras = []
    for idx in range(1, MAX_EXTRA_IMAGES + 1):
        url_field = getattr(form, f'extra_url_{idx}', None)
        file_field = getattr(form, f'extra_{idx}', None)
        url_value = _strip(url_field.data) if url_field else None
        if url_value:
            extras.append(('url', url_value))
            continue
        if file_field and file_field.data and getattr(file_field.data, 'filename', ''):
            extras.append(('file', file_field.data))
    return extras


def log_action(acao):
    if current_user.is_authenticated and current_user.admin:
        log = AdminLog(usuario_id=current_user.id, acao=acao)
        db.session.add(log)
        db.session.commit()


def get_geo_from_ip(ip):
    try:
        return obter_localizacao_por_ip(ip)
    except Exception:
        return None


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = AdminLoginForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data, admin=True).first()
        if user and check_password_hash(user.senha, form.senha.data):
            login_user(user)
            flash('Login de administrador realizado com sucesso!', 'success')
            ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            geo = get_geo_from_ip(ip) or {}
            pais = geo.get('country_name') or geo.get('country')
            cidade = geo.get('city')

            log = AdminLog(admin=current_user.nome, acao="Login no sistema",
                           ip=ip, pais=pais, cidade=cidade)
            db.session.add(log)
            db.session.commit()
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

    produtos_por_marca = db.session.query(
        Produto.marca, func.count(Produto.id)
    ).group_by(Produto.marca).all()

    mes_expr = func.to_char(Pedido.data, 'YYYY-MM')
    vendas_por_mes = (
        db.session.query(mes_expr.label('mes'), func.sum(Pedido.total))
        .group_by(mes_expr)
        .all()
    )

    return render_template(
        'admin/dashboard.html',
        total_produtos=total_produtos,
        total_usuarios=total_usuarios,
        total_pedidos=total_pedidos,
        produtos_por_marca=produtos_por_marca,
        vendas_por_mes=vendas_por_mes
    )


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
        try:
            capa_url = _strip(form.imagem_url.data)
            capa = capa_url if capa_url else None
            if not capa and form.imagem.data and getattr(form.imagem.data, 'filename', ''):
                capa = _save_uploaded_image(form.imagem.data)
        except ValueError as exc:
            flash(str(exc), 'danger')
            return render_template('admin/produtos/form.html', form=form, produto=None)

        produto = Produto(
            nome=form.nome.data,
            marca=form.marca.data,
            descricao=form.descricao.data,
            preco=form.preco.data,
            estoque=form.estoque.data,
            imagem=capa
        )

        extras_inputs = _collect_extra_inputs(form)
        current_order = 0
        for origin, value in extras_inputs[:MAX_EXTRA_IMAGES]:
            if origin == 'url':
                current_order += 1
                produto.imagens.append(ProdutoImagem(filename=value, ordem=current_order))
            else:
                try:
                    stored = _save_uploaded_image(value)
                except ValueError as exc:
                    flash(str(exc), 'danger')
                    return render_template('admin/produtos/form.html', form=form, produto=None)
                current_order += 1
                produto.imagens.append(ProdutoImagem(filename=stored, ordem=current_order))

        db.session.add(produto)
        db.session.commit()
        log_action(f'Adicionou produto {produto.nome}')
        flash('Produto adicionado com sucesso.', 'success')
        return redirect(url_for('admin.produtos'))
    return render_template('admin/produtos/form.html', form=form, produto=None)


@admin_bp.route('/produtos/<int:produto_id>/editar', methods=['GET', 'POST'])
@login_required
def produto_editar(produto_id):
    if not current_user.admin:
        return redirect(url_for('loja.index'))
    produto = Produto.query.get_or_404(produto_id)
    form = ProductForm(obj=produto)
    if form.validate_on_submit():
        try:
            capa_url = _strip(form.imagem_url.data)
            if capa_url:
                produto.imagem = capa_url
            elif form.imagem.data and getattr(form.imagem.data, 'filename', ''):
                produto.imagem = _save_uploaded_image(form.imagem.data)
        except ValueError as exc:
            flash(str(exc), 'danger')
            return render_template('admin/produtos/form.html', form=form, produto=produto)

        form.nome.data and setattr(produto, 'nome', form.nome.data)
        produto.marca = form.marca.data
        produto.descricao = form.descricao.data
        produto.preco = form.preco.data
        produto.estoque = form.estoque.data

        extras_inputs = _collect_extra_inputs(form)
        available_slots = max(0, MAX_EXTRA_IMAGES - len(produto.imagens))
        added = 0
        current_order = max((img.ordem for img in produto.imagens), default=0)

        if extras_inputs and available_slots == 0:
            flash('Este produto já possui o máximo de 4 imagens extras.', 'warning')
        else:
            for origin, value in extras_inputs:
                if added >= available_slots:
                    break
                if origin == 'url':
                    current_order += 1
                    produto.imagens.append(ProdutoImagem(filename=value, ordem=current_order))
                    added += 1
                else:
                    try:
                        stored = _save_uploaded_image(value)
                    except ValueError as exc:
                        flash(str(exc), 'danger')
                        return render_template('admin/produtos/form.html', form=form, produto=produto)
                    current_order += 1
                    produto.imagens.append(ProdutoImagem(filename=stored, ordem=current_order))
                    added += 1
            if extras_inputs and added < len(extras_inputs):
                flash('Algumas imagens extras foram ignoradas pois o limite de 4 foi atingido.', 'warning')

        db.session.commit()
        log_action(f'Editou produto {produto.nome}')
        flash('Produto atualizado.', 'success')
        return redirect(url_for('admin.produtos'))
    return render_template('admin/produtos/form.html', form=form, produto=produto)


@admin_bp.route('/produtos/<int:produto_id>/imagem/<int:imagem_id>/remover', methods=['POST'])
@login_required
def produto_imagem_remover(produto_id, imagem_id):
    if not current_user.admin:
        return redirect(url_for('loja.index'))

    produto = Produto.query.get_or_404(produto_id)
    imagem = ProdutoImagem.query.filter_by(id=imagem_id, produto_id=produto.id).first_or_404()

    db.session.delete(imagem)
    db.session.commit()

    log_action(f'Removeu imagem extra {imagem_id} do produto {produto.nome}')
    flash('Imagem extra removida.', 'info')
    return redirect(url_for('admin.produto_editar', produto_id=produto.id))


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
    query = Pedido.query.join(Usuario)
    if form.validate_on_submit():
        if form.status.data and form.status.data != 'todos':
            query = query.filter(Pedido.status == form.status.data)
        if form.cliente.data:
            query = query.filter(Usuario.nome.ilike(f"%{form.cliente.data}%"))
        if form.data_inicio.data:
            inicio = datetime.combine(form.data_inicio.data, time.min)
            query = query.filter(Pedido.data >= inicio)
        if form.data_fim.data:
            fim = datetime.combine(form.data_fim.data, time.max)
            query = query.filter(Pedido.data <= fim)
    pedidos = query.order_by(Pedido.data.desc()).all()
    return render_template('admin/pedidos/lista.html', pedidos=pedidos, form=form)


@admin_bp.route('/pedidos/exportar_csv')
@login_required
def pedidos_exportar_csv():
    if not current_user.admin:
        return redirect(url_for('loja.index'))
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Cliente', 'Data', 'Total', 'Status'])
    for p in Pedido.query.order_by(Pedido.data.desc()).all():
        writer.writerow([p.id, p.usuario.nome, p.data.strftime('%Y-%m-%d %H:%M'), f'{p.total:.2f}', p.status])
    output.seek(0)
    return Response(output.read(), mimetype='text/csv',
                    headers={'Content-Disposition': 'attachment; filename=pedidos.csv'})


@admin_bp.route('/pedidos/<int:pedido_id>')
@login_required
def pedido_detalhe(pedido_id):
    if not current_user.admin:
        return redirect(url_for('loja.index'))
    pedido = Pedido.query.get_or_404(pedido_id)
    return render_template('admin/pedidos/detalhe.html', pedido=pedido)


@admin_bp.route('/usuarios')
@login_required
@restrito_por_ip
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
