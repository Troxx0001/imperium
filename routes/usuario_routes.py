from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from models.usuario import Usuario
from models import db

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = generate_password_hash(request.form['senha'])

        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        db.session.add(novo_usuario)
        db.session.commit()
        flash("Cadastro realizado com sucesso.")
        return redirect(url_for('auth.login'))

    return render_template('registro.html')