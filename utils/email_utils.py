from flask_mail import Message

def enviar_email(destinatario, assunto, corpo_html):
    from app import mail, app  # Importa só quando a função é chamada
    with app.app_context():
        msg = Message(assunto,
                      sender='no-reply@imperium.com',
                      recipients=[destinatario])
        msg.html = corpo_html
        mail.send(msg)