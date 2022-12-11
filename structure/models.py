#models.py
from structure import db,login_manager,app
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime
# from sqlalchemy import create_engine, Table, MetaData
# metadata = MetaData()

class User(db.Model,UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    profile_image = db.Column(db.String(64),nullable=False,default='default_profile.png')
    email = db.Column(db.String(64),unique=True,index=True)
    name = db.Column(db.String(64),nullable=True)
    role = db.Column(db.String(64),nullable=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))
    verification = db.Column(db.String(5))
    verification_code = db.Column(db.String(100))


    def __init__(self,email,username,password,name,role,verification_code,verification):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.name = name
        self.role = role
        self.verification = verification
        self.verification_code = verification_code

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
    # __table__ = Table('event', metadata, schema='public')
    __tablename__ = "event"
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
    views = db.Column(db.Integer, nullable=True,default=0)
    tags = db.Column(db.JSON,nullable=True)
    eventtags = db.Column(db.String(200))
    baseprice = db.Column(db.Integer, nullable=True)
    users = db.relationship('User',backref='event',lazy=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=True)


# Define the database schema for tickets
class Ticket(db.Model):
    __tablename__ = "tickets"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=True)
    price = db.Column(db.Float, nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    day = db.Column(db.String, nullable=True)
    features = db.Column(db.String(255), nullable=True)
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


# class Purchase(db.Model):
#     __tablename__ = 'purchases'
#     id = db.Column(db.Integer, primary_key=True)
#     ticket_id = db.Column(db.Integer,db.ForeignKey('ticket.id'))
#     ticket = db.relationship('Ticket', backref=db.backref('purchases', lazy=True))
    

class Cart(db.Model):
    __tablename__ = "carts"

    cart_id = db.Column(db.Integer, primary_key=True)
    total_price = db.Column(db.Float)
    transaction_id = db.Column(db.String(100))
    items = db.relationship("Item", backref="cart")
    status = db.Column(db.String(15))
    reference = db.Column(db.String(200))

    def __init__(self, total_price,status,transaction_id,reference):
        self.total_price = total_price
        self.status = status
        self.transaction_id = transaction_id
        self.reference = reference

    def to_dict(self):
        return {
            "cart_id": self.cart_id,
            "total_price": self.total_price,
            "status": self.status,
            "items": [item.to_dict() for item in self.items]
        }


class Item(db.Model):
    __tablename__ = "items"

    item_id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.cart_id"))
    event_id = db.Column(db.Integer)
    events_id  = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=True)
    event = db.relationship('Event', backref=db.backref('items', lazy=True,uselist=False))
    tickets_id  = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=True)
    ticket = db.relationship('Event', backref=db.backref('ticketitems', lazy=True,uselist=False,overlaps="event,items"))
    tickets = db.relationship('Ticket', backref=db.backref('items', lazy=True,uselist=False))
    ticket_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    reference = db.Column(db.String(200))
    users = db.relationship('User',backref='items',lazy=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=True)
    
    def __init__(self, cart_id, event_id, quantity, price,ticket_id,reference,user_id,events_id,tickets_id):
        self.cart_id = cart_id
        self.event_id = event_id
        self.quantity = quantity
        self.price = price
        self.ticket_id = ticket_id
        self.reference = reference
        self.user_id = user_id
        self.tickets_id = tickets_id
        self.events_id = events_id

    def total_price(self):
        return self.quantity * self.price

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "cart_id": self.cart_id,
            "event_id": self.event_id,
            "quantity": self.quantity,
            "price": self.price,
            "total_price": self.total_price()
        }

# s
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
