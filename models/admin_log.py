from datetime import datetime
from models import db

class AdminLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    acao = db.Column(db.String(255), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    ip = db.Column(db.String(100))  # IP do administrador
    cidade = db.Column(db.String(100))  # Cidade do administrador
    pais = db.Column(db.String(100))  # País do administrador
    usuario = db.relationship('Usuario')
#CRIAR LOG DE ONDE O ADM FEZ A ALTERAÇÃO