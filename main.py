import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from functools import wraps
import shutil
from PIL import Image
import jwt
import pytz
from dataclasses import dataclass
from celery import Celery
from celery.result import AsyncResult
from celery.schedules import crontab
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from functools import wraps

current_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "application/data/e-library.db")

db = SQLAlchemy()
db.init_app(app)
app.app_context().push()
app.secret_key = "3012419"
Tz = pytz.timezone("Asia/Calcutta")

celery = Celery("main", broker="redis://localhost:6379/1", backend="redis://localhost:6379/2")
celery.conf.timezone = 'UTC'
celery.conf.enable_utc = True


class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)

celery.Task = ContextTask
app.app_context().push()





####### MODELS #######




@dataclass
class Users(db.Model):
  __tablename__ = "Users"
  Id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
  Name: str = db.Column(db.String, nullable=False, unique=True)
  Email: str = db.Column(db.String, nullable=False)
  Password: str = db.Column(db.String, nullable=False)
  Authorisation: str = db.Column(db.String, nullable=False)
  LastLogin: str = db.Column(db.String, nullable=False)

@dataclass
class Sections(db.Model):
  __tablename__ = "Sections"
  Id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
  Name: str = db.Column(db.String, nullable=False, unique=True)
  Description: str = db.Column(db.String)
  AdminId: int = db.Column(db.Integer,db.ForeignKey("Users.Id"),nullable=False)

@dataclass
class Books(db.Model):
  __tablename__ = "Books"
  Id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
  Name: str = db.Column(db.String, nullable=False)
  SectionId: int = db.Column(db.Integer,db.ForeignKey("Sections.Id"),nullable=False)
  SectionName: int = db.Column(db.Integer,db.ForeignKey("Sections.Name"),nullable=False)
  Author: str = db.Column(db.String, nullable=False)
  Content: str = db.Column(db.String, nullable=False)
  Price: int = db.Column(db.Integer, nullable=False)
  DateIssued: str = db.Column(db.String, nullable=False)

@dataclass
class MyBooks(db.Model):
  __tablename__ = "MyBooks"
  Id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
  UserId: int = db.Column(db.Integer,db.ForeignKey("Users.Id"),nullable=False)
  BookId: int = db.Column(db.Integer,db.ForeignKey("Books.Id"),nullable=False)
  DateIssued: str = db.Column(db.String, nullable=False)
  RevokeDate: str = db.Column(db.String, nullable=False)
  Revoked: bool = db.Column(db.Boolean,default=True)
  Total: str = db.Column(db.Integer,nullable=False)

@dataclass
class Feedback(db.Model):
   __tablename__ = "Feedback"
   Id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
   BookId: int = db.Column(db.Integer,db.ForeignKey("Books.Id"),nullable=False)
   UserId: int = db.Column(db.Integer,db.ForeignKey("Users.Id"),nullable=False)
   Feedback: str = db.Column(db.String, nullable=False)
   Verified: bool = db.Column(db.Boolean,default=False)



def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({"Alert": "Token not found"})
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            user = Users.query.filter_by(Id=payload["uid"]).first()
            uid = user.Id
            authorisation = user.Authorisation
        except:
            return jsonify({"Alert": "Invalid Token"})
        return func(uid,authorisation,*args, **kwargs)
    return decorated






# ~/go/bin/MailHog
# sudo service redis-server start
# celery -A main.celery worker -l info
# celery -A main.celery beat -l info

@app.route('/exportbook/<int:bid>', methods=["GET"])
@token_required
def exportbook(uid,authorisation,bid):
    
    job = export_book.delay(uid, bid)
    
    return jsonify({
        "uid":uid,
        "bid":bid,
        "tid":job.task_id
    })


@app.route('/taskstatus/<taskid>', methods=["GET"])
@token_required
def taskstatus(uid,authorisation,taskid):
    task = AsyncResult(taskid, app=celery)
    return str(task.successful())


def send_email(to, subject, message, attachment_path=None):
    msg = MIMEMultipart()
    msg["From"] = "library@gmail.com"
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(message,"html"))

    if attachment_path != None:
        attachment_file = open(attachment_path,'r')
        part = MIMEApplication(
                    attachment_file.read(),
                    Name='Monthly Report'
                )
        part['Content-Disposition'] = 'attachment; filename="Monthly Report.html"'
        msg.attach(part)

    s = smtplib.SMTP("localhost" ,1025)
    s.set_debuglevel(1)
    s.login("elibrary@gmail.com", "sanjay")
    s.send_message(msg)
    s.quit()

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    sender.add_periodic_task(
        crontab(hour='*', minute='*/1'),
        send_alert.s()
    )
    sender.add_periodic_task(
        crontab(hour='*', minute='*/1'),
        send_monthly_reports.s()
    )

@celery.task()
def send_alert():
    userlist = Users.query.filter_by(Authorisation = 'user').all()
    today = datetime.datetime.now(Tz).date()
    for user in userlist:
        last_login = datetime.datetime.strptime(user.LastLogin,"%Y-%m-%d").date()
        if last_login != today:
            send_email(user.Email, "Daily Alert", f"Hey {user.Name}, login now to check out exciting new arrivals.")


#Celery Async Jobs
@celery.task()
def export_book(uid, bookid): 
    book = Books.query.filter_by(Id = bookid).first()
    head = f"""<head><meta charset="UTF-8"><meta name="color-scheme" content="light dark"><title align='center'>{book.Name}</title><link href="/src/assets/style.css" rel="stylesheet" type="text/css" /><meta name="viewport" content="width=device-width"></head>"""
    content = f"<body><h2>{book.Name}</h2><p>{book.Content}</p></body>"
    book_file = open(f"./frontend/src/assets/exports/{book.Name} by {book.Author}.html","w")
    book_file.write(head+content)
    book_file.close()


@celery.task()
def send_monthly_reports():
    users = Users.query.filter_by(Authorisation="user").all()
    for user in users:
        monthly_report(user.Id)        
        send_email(user.Email, "Monthly Report", f"Hey {user.Name}, here is your monthly report.",f"./frontend/src/assets/reports/{user.Name}_monthly_report.html")

def monthly_report(uid): 
    my_books = MyBooks.query.filter_by(UserId = uid).all()
    user = Users.query.filter_by(Id = uid).first()
    head = f"""<head><meta charset="UTF-8"><meta name="color-scheme" content="light dark"><title align='center'>{user.Name}</title><link href="/src/assets/style.css" rel="stylesheet" type="text/css" /><meta name="viewport" content="width=device-width"></head>"""
    book_file = open(f"./frontend/src/assets/reports/{user.Name}_monthly_report.html","w")
    book_file.write(head+'<body>')
    intro = f"<h1>Monthly Report for {user.Name}. The following are the books you have currently.</h1>"
    book_file.write(intro)
    for my_book in my_books:
        book = Books.query.filter_by(Id=my_book.BookId).first()
        content = f"<h2>{book.Name}</h2><br>"
        book_file.write(content)
    book_file.write('</body>')
    book_file.close()    

from application.controllers.user_crud import *
from application.controllers.admin_crud import *

if __name__ == "__main__":
  app.run(debug=True)