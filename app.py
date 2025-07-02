from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from models import db  # use o db do models
from models.usuario import Usuario
from routes import loja_routes, auth_routes, api_routes
from routes.admin_routes import admin_bp
from routes.loja_routes import loja
from routes.carrinho_routes import carrinho_bp
from routes.usuario_routes import usuario_bp
from itsdangerous import URLSafeTimedSerializer
from flask import flash, redirect, request, render_template, url_for
from werkzeug.security import generate_password_hash
from utils.email_utils import enviar_email
    
app = Flask(__name__)
app.config.from_object('config.Config')
app.secret_key = 'sua-chave-secreta'  # Adicionando a chave secreta

# Looking to send emails in production? Check out our Email API/SMTP product!
app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '9308d9fabc9dd9'
app.config['MAIL_PASSWORD'] = '449db778deda39'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

db.init_app(app)  # só inicializa, não crie outro db!
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # redireciona para login se não autenticado

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Registra os blueprints
app.register_blueprint(auth_routes.bp)
app.register_blueprint(api_routes.bp)
app.register_blueprint(loja)
app.register_blueprint(carrinho_bp, url_prefix='/carrinho')
app.register_blueprint(usuario_bp)
app.register_blueprint(admin_bp)

mail = Mail(app)
serializer = URLSafeTimedSerializer(app.secret_key)


if __name__ == '__main__':
    app.run()

