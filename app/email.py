from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    #mail.send(msg)
    Thread(target=send_async_email,
           args=(current_app._get_current_object(), msg)).start()


"""
Выражение current_app._get_current_object() извлекает фактический 
экземпляр приложения из объекта прокси, так что это то, что я передал 
потоку в качестве аргумента.
"""