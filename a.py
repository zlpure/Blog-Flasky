from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)

app.config.update(
MAIL_SERVER='smtp.163.com',
MAIL_PORT=465,
MAIL_USE_SSL=True,
MAIL_USERNAME = '18302882633',
MAIL_PASSWORD = 'zl123456')

mail = Mail(app)
@app.route("/")
def index():
    msg = Message(subject="helloworld", sender='18302882633@163.com', recipients=['470329591@qq.com'])
    msg.html = "testinghtml"
    mail.send(msg)
    return 'hello'

if __name__ =='__main__':
    app.run(debug=True)
