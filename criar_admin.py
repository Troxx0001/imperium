from app import app, db
from models.usuario import Usuario
from werkzeug.security import generate_password_hash

with app.app_context():
    admin = Usuario(
        nome="teste",
        email="teste@gmail.com",
        senha=generate_password_hash("123"),
        admin=True
    )
    db.session.add(admin)
    db.session.commit()
    print("Administrador criado com sucesso.")