from flask import render_template,request,Blueprint,redirect,url_for,session,current_app
from structure.models import User ,WebFeature,Event , Ticket ,Article ,NewsletterEmails ,Newsletter ,About, Cart,Item
from structure import db,app
from structure.web.forms import NewsletterSubForm
from sqlalchemy.orm import load_only
from flask_login import login_required
import secrets
import os
import datetime 
import calendar
from sqlalchemy import extract,func,and_,text
from sqlalchemy.types import Unicode
from flask_mail import Message,Mail
import random

userportal = Blueprint('userportal',__name__)


@userportal.route('/mytickets')
def mytickets():
    user = User.query.filter_by(id=session['id']).first()
    print(user.email)
    tickets = Item.query.filter_by(user_id=user.id).all()
    print(tickets)
    mytickets = []
    # if tickets:
    for ticket in tickets:
        tick = Ticket.query.filter_by(id=ticket.ticket_id).first()
        print(tick.event)
        mytickets.append({'name': tick.name, 'price': tick.price,'ticket_id':tick.id,'eventname':tick.event.name,'location':tick.event.location,'date':tick.event.date,'quantity':1,'image':tick.image,'event_id':tick.event_id})   
    print(mytickets)
    return render_template('userportal/mytickets.html')
