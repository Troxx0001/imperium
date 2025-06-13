import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'sua-chave-secreta')
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI',
        'postgresql://postgres:5Phwwm1iIaD4@localhost:5432/imperium_utf8',
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
