from datetime import datetime
from models import db

class AdminLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    acao = db.Column(db.String(255), nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    ip = db.Column(db.String(100))  
    cidade = db.Column(db.String(100))  
    pais = db.Column(db.String(100))  
    usuario = db.relationship('Usuario')
