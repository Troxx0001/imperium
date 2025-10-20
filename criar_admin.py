from app import app, db
from models.usuario import Usuario
from werkzeug.security import generate_password_hash

with app.app_context():
    if not Usuario.query.filter_by(email="admin@admin.com").first():
        admin = Usuario(
            nome="Administrador",
            email="administrador@admin.com",
            senha=generate_password_hash("123"), 
            admin=True,                
            verificado=True            
        )   
        db.session.add(admin)
        db.session.commit()
        print("Administrador criado com sucesso.")  
    else:
        print("Administrador já existe.")