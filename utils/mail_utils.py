from flask import current_app
from flask_mail import Message


def send_email(to: str, subject: str, html: str) -> None:
    mail = current_app.extensions.get('mail')
    if mail is None:
        raise RuntimeError('Flask-Mail não está configurado no aplicativo atual.')

    msg = Message(
        subject=subject,
        recipients=[to],
        html=html,
        sender=current_app.config.get('MAIL_DEFAULT_SENDER'),
    )
    mail.send(msg)
