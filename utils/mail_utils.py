from flask_mail import Message
from flask import current_app


def send_email(to: str, subject: str, html: str) -> None:
    mail = current_app.extensions.get('mail')
    if mail is None:
        raise RuntimeError('Flask-Mail extension is not initialized.')

    message = Message(
        subject=subject,
        recipients=[to],
        html=html,
        sender=current_app.config.get("MAIL_DEFAULT_SENDER"),
    )
    mail.send(message)
