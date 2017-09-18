#coding=utf-8
from flask import Flask,render_template,session,redirect,url_for,flash
from flask_script import Manager,Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from flask_migrate import Migrate,MigrateCommand
from wtforms import StringField,SubmitField
from wtforms.validators import Required,Regexp
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail,Message
from threading import Thread
from celery import Celery
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'zengliang123456@gmail.com'
app.config['MAIL_PASSWORD'] = 'ZL19950824!!'
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'zengliang123456@gmail.com'
app.config['FLASKY_ADMIN']  = 'zengliang123456@gmail.com'

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
mail = Mail(app)

migrate = Migrate(app,db)


class NameForm(Form):
    name = StringField('What is your name?',validators=[Regexp('\w+')]) #wei kong
    submit = SubmitField('Submit')

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True,nullable=False)
    users = db.relationship('User',backref='role',lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' %self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self):
        return  '<User %r>' %self.username

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)
manager.add_command('shell',Shell(make_context=make_shell_context))
manager.add_command('db',MigrateCommand)

async_task = Celery('tasks', broker='amqp://guest@localhost//')

@async_task.task()
def send_async_mail(app,msg):
    with app.app_context():
        mail.send(msg)

def send_mail(to,subject,template,**kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX']+subject,recipients=[to],
                  sender=app.config['FLASKY_MAIL_SENDER'])
    msg.body = render_template(template+'.txt',**kwargs)
    msg.html = render_template(template+'.html',**kwargs)
    thr = Thread(target=send_async_mail,args=[app,msg])
    thr.start()
    return thr
    #mail.send(msg)

@app.route('/',methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            flash('you have change your name')
            if app.config['FLASKY_ADMIN']:
                send_mail(app.config['FLASKY_ADMIN'],'New User','mail/new_user',user=user)
        else:
            session['known'] = True
            #flash('Looks like you have changed name!')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',form=form,name=session.get('name'),current_time=datetime.utcnow(),known=session.get('known',False))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def inteenal_server_error(e):
    return render_template('500.html'),500

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

if __name__ == '__main__':
    manager.run()
    #app.run(host='0.0.0.0',debug=True)