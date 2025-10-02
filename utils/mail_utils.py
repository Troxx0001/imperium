from flask_mail import Message
from flask import current_app

def send_email(to: str, subject: str, html: str) -> None:
    from app import mail

    message = Message(
        subject=subject,
        recipients=[to],
        html=html,
        sender=current_app.config.get("MAIL_DEFAULT_SENDER"),
    )
    mail.send(message)
