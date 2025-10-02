from flask import Blueprint, render_template, redirect, url_for, flash, request
from models.usuario import Usuario
from models import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from utils.email_utils import enviar_email
from utils.ipapi_utils import obter_localizacao_por_ip
from models.admin_log import AdminLog
from forms import (
    RegisterForm,
    LoginForm,
    RequestResetForm,
    ResetPasswordForm,
    ChangePasswordForm,
)
from utils.token_utils import generate_token, confirm_token
from utils.mail_utils import send_email


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        senha = form.senha.data
        user = Usuario.query.filter_by(email=email).first()
        if user and check_password_hash(user.senha, senha):
            if not user.verificado:
                flash('Você precisa confirmar seu e-mail antes de fazer login.', 'warning')
                return redirect(url_for('auth.login'))
            login_user(user)
            ip = request.remote_addr
            localizacao = obter_localizacao_por_ip(ip)
            log = AdminLog(
                usuario_id=user.id,
                acao="Login no sistema",
                ip=ip,
                cidade=localizacao.get('city') if localizacao else 'Desconhecida',
                pais=localizacao.get('country_name') if localizacao else 'Desconhecido'
            )
            db.session.add(log)
            db.session.commit()
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for('loja.index'))
        flash('Login inválido', 'danger')
    return render_template('login.html', form=form)

@bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    form = RegisterForm()
    if form.validate_on_submit():
        from app import serializer  # Importa dentro da função para evitar import circular

        nome = form.nome.data.strip()
        email = form.email.data.lower()
        senha = generate_password_hash(form.senha.data)

        if Usuario.query.filter_by(email=email).first():
            flash("Este e-mail já está em uso. Tente outro.", "danger")
            return render_template("cadastro.html", form=form)

        if Usuario.query.filter_by(nome=nome).first():
            flash("Este nome de usuário já está em uso. Escolha outro.", "danger")
            return render_template("cadastro.html", form=form)

        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()

        token = serializer.dumps(email, salt='email-confirmacao')
        link_confirmacao = url_for('auth.confirmar_email', token=token, _external=True)
        corpo_email = f'''
        <h1>Confirme sua conta</h1>
        <p>Clique no link abaixo para ativar sua conta:</p>
        <a href="{link_confirmacao}">Ativar Conta</a>
        '''
        enviar_email(email, 'Confirmação de Conta', corpo_email)

        flash("Cadastro realizado com sucesso! Verifique seu e-mail.", "success")
        return redirect(url_for('auth.login'))

    return render_template("cadastro.html", form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout realizado com sucesso.", "info")
    return redirect(url_for('auth.login'))

@bp.route('/confirmar/<token>')
def confirmar_email(token):
    from app import serializer
    try:
        email = serializer.loads(token, salt='email-confirmacao', max_age=3600)
    except Exception:
        return 'Token inválido ou expirado.'

    usuario = Usuario.query.filter_by(email=email).first()
    if usuario:
        usuario.verificado = True
        db.session.commit()
        return 'Conta confirmada com sucesso!'
    else:
        return 'Usuário não encontrado.'


@bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password_request():
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = generate_token(user.email)
            reset_link = url_for('auth.reset_password_token', token=token, _external=True)
            html = render_template(
                'emails/reset_password.html', user=user, reset_link=reset_link
            )
            send_email(user.email, 'Recuperação de senha - Imperium', html)
        flash('Se o e-mail existir, enviaremos um link de recuperação.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', form=form)


@bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password_token(token):
    email = confirm_token(token)
    if not email:
        flash('Link inválido ou expirado.', 'danger')
        return redirect(url_for('auth.reset_password_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = Usuario.query.filter_by(email=email.lower()).first_or_404()
        user.senha = generate_password_hash(form.senha.data)
        db.session.commit()
        flash('Senha alterada com sucesso. Faça login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_form.html', form=form)


@bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not check_password_hash(current_user.senha, form.atual.data):
            flash('Senha atual incorreta.', 'danger')
        else:
            current_user.senha = generate_password_hash(form.nova.data)
            db.session.commit()
            flash('Senha atualizada.', 'success')
            return redirect(url_for('loja.meus_pedidos'))
    return render_template('auth/change_password.html', form=form)
