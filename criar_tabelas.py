from app import app, db  # Certifique-se que 'app' e 'db' estão exportados no app.py

with app.app_context():
    db.create_all()
    print("Tabelas criadas com sucesso.")
