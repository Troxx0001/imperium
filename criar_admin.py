from app import app, db
from models.usuario import Usuario
from werkzeug.security import generate_password_hash

with app.app_context():
    if not Usuario.query.filter_by(email="admin@admin.com").first():
        admin = Usuario(
            nome="ADM",
            email="adm123@admin.com",
            senha=generate_password_hash("admin123"),  # senha segura
            admin=True,                # campo correto para admin
            verificado=True            # campo correto para e-mail confirmado
        )   
        db.session.add(admin)
        db.session.commit()
        print("Administrador criado com sucesso.")
    else:
        print("Administrador já existe.")