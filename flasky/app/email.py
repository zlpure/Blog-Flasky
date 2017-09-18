from flask_mail import Mail,Message
from threading import Thread
from celery import Celery
from flask import Flask,render_template,session,current_app
from . import mail

#async_task = Celery('tasks', broker='amqp://guest@localhost//')

#@async_task.task()
def send_async_mail(app,msg):
    with app.app_context():
        mail.send(msg)

def send_mail(to,subject,template,**kwargs):
    app = current_app._get_current_object()
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,recipients=[to],
                  sender=app.config['FLASKY_MAIL_SENDER'])
    msg.body = render_template(template+'.txt',**kwargs)
    msg.html = render_template(template+'.html',**kwargs)
    thr = Thread(target=send_async_mail,args=[app,msg])
    thr.start()
    return thr
