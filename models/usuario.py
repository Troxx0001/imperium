from flask_login import UserMixin
from models import db

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    admin = db.Column(db.Boolean, default=False)  # NOVO CAMPO
    verificado = db.Column(db.Boolean, default=False)

    @classmethod
    def get(cls, user_id):
        return cls.query.get(int(user_id))
