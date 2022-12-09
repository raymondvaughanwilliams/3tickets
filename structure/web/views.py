from flask import render_template,request,Blueprint,redirect,url_for,session,current_app
from structure.models import User ,WebFeature,Event , Ticket ,Article ,NewsletterEmails ,Newsletter ,About
from structure import db,photos
from structure.web.forms import NewsletterSubForm
from sqlalchemy.orm import load_only
from flask_login import login_required
import secrets
import os
import datetime 
import calendar
from sqlalchemy import extract,func,and_,text
from sqlalchemy.types import Unicode

web = Blueprint('web',__name__)


@web.route('/homepage')
def homepage():
    '''
    This is the home page view. Notice how it uses pagination to show a limited
    number of posts by limiting its query size and then calling paginate.
    '''
    newsletterform = NewsletterSubForm()
    date = datetime.datetime.now()
    daysoftheweek = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    day = datetime.datetime.today().weekday()
    day = daysoftheweek[day]
    date = date.strftime("%m %b %Y")
    page = request.args.get('page', 1, type=int)
    events = Event.query.all()
    articles = Article.query.all()
    web_features = WebFeature.query.order_by(WebFeature.date.desc()).paginate(page=page, per_page=10)
    about = About.query.filter_by(id=1).first()
    

    curr_date= datetime.datetime.now()
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    months=["January","February","March","April","May","June","July","August","September","October","November","December","January","February","March","April","May","June"]
    upcoming_months= [] 
    current_month_index = current_month - 1
    for i in range(current_month_index, current_month_index+5):
        # Append each of the next four months to the list of upcoming months
        upcoming_months.append(months[i])
    records = Event.query.all()
    current_month_events = []
    for record in records:
        if record.date.strftime('%Y-%m-%d %H:%M:%S') > curr_date.strftime('%Y-%m-%d %H:%M:%S') and int(record.date.strftime('%m')) == current_month:
            current_month_events.append(record)
    one_month_events = []
    for record in records:
        nxt_month = current_month + 1
        if nxt_month > 12:
            nxt_month = nxt_month - 12
        if record.date.strftime('%Y-%m-%d %H:%M:%S') > curr_date.strftime('%Y-%m-%d %H:%M:%S') and int(record.date.strftime('%m')) == nxt_month:
            one_month_events.append(record)
    two_month_events = []
    for record in records:
        the_month = current_month + 2
        if the_month > 12:
            the_month = the_month - 12
        if record.date.strftime('%Y-%m-%d %H:%M:%S') > curr_date.strftime('%Y-%m-%d %H:%M:%S') and int(record.date.strftime('%m')) == the_month:
            two_month_events.append(record)

    

    return render_template('web/homepage.html',web_features=web_features,events=events,articles=articles,date=date,upcoming_months=upcoming_months,current_month_events=current_month_events,one_month_events=one_month_events,two_month_events
                           =two_month_events,newsletterform=newsletterform,about=about)
    


@web.route('/schedule')
def schedule():
    category = request.args.get('category')
    x = "music"
    x = '%{0}%'.format(x)
    events_by_category = Event.query.filter(Event.eventtags.like(x)).all()
    allevents = Event.query.all()
    print (events_by_category)
    
    
    # if request.args.get('status') == "successful":
            # destination_json = json.dumps(data)

    #     transaction_id = request.args.get('transaction_id')
    #     # user = User.query.filter_by(email=session['email']).first()
    #     status = request.args.get('status')
    return render_template('web/schedule.html',allevents=allevents)


@web.route('/suscribetonewsletter',methods=['GET', 'POST'])
def suscribetonewsletter():
    form = NewsletterSubForm()
    if request.method == 'POST':
        email = form.email.data
        
        sub = NewsletterEmails(email=email, status="yes")
        db.session.add(sub)
        db.session.commit()
        # flash(f'Meme added successfully','success')
        return redirect(url_for('web.homepage'))
    
    


@web.route('/eventdetails/<int:event_id>',methods=['GET', 'POST'])
def event(event_id):
    form = NewsletterSubForm()
    event =  Event.query.filter(Event.id == event_id).first()
    tickets = Ticket.query.filter(Ticket.event_id == event_id).all()
    print(event)
    tickettabs = []
    for ticket in tickets:
        appendage = "ticket" + str(ticket.id)
        print(appendage)
        tickettabs.append(appendage)
        # flash(f'Meme added successfully','success')
    print(tickettabs)
    return render_template('web/event.html',event=event,tickets=tickets,tickettabs=tickettabs)