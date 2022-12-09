#models.py
from structure import db,login_manager,app
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime


class User(db.Model,UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    profile_image = db.Column(db.String(64),nullable=False,default='default_profile.png')
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))


    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"Username {self.username}"


class WebFeature(db.Model):


    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    title = db.Column(db.String(140),nullable=False)
    wtext = db.Column(db.Text,nullable=False)


    def __init__(self,title,wtext):
        self.title = title
        self.wtext = wtext

    def __repr__(self):
        return f"Post ID: {self.id} -- Date: {self.date} --- {self.title}---{self.text}"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    date = db.Column(db.Date, nullable=True)
    time = db.Column(db.Time, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    days = db.Column(db.Integer, nullable=True)
    image1 = db.Column(db.String(100), nullable=True)
    image2 = db.Column(db.String(100), nullable=True)
    image3 = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), nullable=True)
    number = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    views = db.Column(db.Integer, nullable=True)
    tags = db.Column(db.JSON,nullable=True)
    eventtags = db.Column(db.String(200))
    baseprice = db.Column(db.Integer, nullable=True)


# Define the database schema for tickets
class Ticket(db.Model):
    __tablename__ = "tickets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=True)
    price = db.Column(db.Float, nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    day = db.Column(db.String, nullable=True)
    image = db.Column(db.String(50))
    event = db.relationship('Event', backref=db.backref('tickets', lazy=True,uselist=False))



class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    views = db.Column(db.Integer)
    likes = db.Column(db.Integer)
    image = db.Column(db.String(50))
    date = db.Column(db.Date,nullable=True,default=datetime.utcnow)

    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=True)
    event = db.relationship('Event', backref=db.backref('articles', lazy=True))



class About(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    address = db.Column(db.String(50))
    number = db.Column(db.String(20), nullable=True)
    instagram = db.Column(db.String(50))
    twitter = db.Column(db.String(50))
    email = db.Column(db.String(30))
    
    
class NewsletterEmails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(5),nullable=True)
    

class Newsletter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(60))
    body = db.Column(db.String(20))
    recepients = db.Column(db.JSON)
    date = db.Column(db.Date, nullable=True,default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
