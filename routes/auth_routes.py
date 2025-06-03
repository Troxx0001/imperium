from flask import Blueprint, render_template, redirect, url_for, flash, request
from models.usuario import Usuario
from models import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from utils.email_utils import enviar_email

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        user = Usuario.query.filter_by(email=email).first()
        if user and check_password_hash(user.senha, senha):
            if not user.verificado:
                flash('Você precisa confirmar seu e-mail antes de fazer login.', 'warning')
                return redirect(url_for('auth.login'))
            login_user(user)
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for('loja.index'))
        flash('Login inválido')
    return render_template('login.html')

@bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        from app import serializer  # <-- Adicione esta linha aqui
        nome = request.form['nome']
        email = request.form['email']
        senha = generate_password_hash(request.form['senha'])   
        novo = Usuario(nome=nome, email=email, senha=senha)
        db.session.add(novo)
        db.session.commit()

        token = serializer.dumps(email, salt='email-confirmacao')
        link_confirmacao = url_for('auth.confirmar_email', token=token, _external=True)

        corpo_email = f'''
        <h1>Confirme sua conta</h1>
        <p>Clique no link abaixo para ativar sua conta:</p>
        <a href="{link_confirmacao}">Ativar Conta</a>
        '''

        enviar_email(email, 'Confirmação de Conta', corpo_email)
        return redirect(url_for('auth.login'))  
    return render_template('cadastro.html')

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
