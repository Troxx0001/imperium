import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_mail import Mail
from flask_migrate import Migrate
from models import db  
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
    
load_dotenv()

app = Flask(__name__)
app.config.from_object('config.Config')
app.secret_key = 'sua-chave-secreta'
app.config['SECRET_KEY'] = app.secret_key

def _bool_env(name: str, default: str = 'False') -> bool:
    return os.getenv(name, default).lower() in {'true', '1', 't', 'yes'}


app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'sandbox.smtp.mailtrap.io')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 2525))
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', '9308d9fabc9dd9')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '449db778deda39')
app.config['MAIL_USE_TLS'] = _bool_env('MAIL_USE_TLS', 'True')
app.config['MAIL_USE_SSL'] = _bool_env('MAIL_USE_SSL', 'False')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'Imperium <no-reply@imperium.com>')

db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
csrf = CSRFProtect()
csrf.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

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

