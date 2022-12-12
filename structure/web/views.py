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
from sqlalchemy import  and_, or_ ,desc ,asc
web = Blueprint('web',__name__)



app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "raymondvaughanwilliams@gmail.com"
app.config["MAIL_PASSWORD"] = "mowfdigzaouywugg"

mail = Mail(app) 

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
    # events = Event.query.all()
    events = Event.query.filter(and_(Event.date > datetime.date.today())).order_by(desc(Event.date)).all()

    articles = Article.query.all()
    web_features = WebFeature.query.order_by(WebFeature.date.desc()).paginate(page=page, per_page=10)
    about = About.query.filter_by(id=1).first()
    
    eventsschedulelink = " url_for('web.eventsschedule')"
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
    print(records)
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
                           =two_month_events,newsletterform=newsletterform,about=about,eventsschedulelink=eventsschedulelink)
    


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
    # if event.date < datetime.datetime.now():
    #     finished = "yes"
    # else:
    #     finished = "no"
    tickets = Ticket.query.filter(Ticket.event_id == event_id).all()
    print(event)
    event.views =event.views + 1
    db.session.commit()
    return render_template('web/event.html',event=event,tickets=tickets)


@web.before_request
def create_cart():
    # If the cart doesn't exist in the session, create it
    if 'cart' not in session:
        session['cart'] = []


# cart =[]

@web.route('/add_to_cart', methods=['POST','GET'])
def add_to_cart():
    # Get the item name and price from the form data
    item_name = request.args.get('name')
    item_price = request.args.get('price')
    item_id = request.args.get('id')
    print(item_name)
    ticket = Ticket.query.filter(Ticket.id == item_id).first()

    # Add the item to the cart
    session['cart'] .append({'name': item_name, 'price': item_price,'ticket_id':item_id,'eventname':ticket.event.name,'location':ticket.event.location,'date':ticket.event.date,'quantity':1,'image':ticket.image,'event_id':ticket.event_id})
    session.modified = True
    print(session['cart'] )
    return redirect(url_for('web.homepage'))



@web.route('/cart')
@login_required
def cart():
    print(session['id'])
    user = User.query.filter(User.id == session['id']).first()
    carttickets= []
    for item in session['cart']:
        print(item['ticket_id'])
        ticket = Ticket.query.filter(Ticket.id == item['ticket_id']).first()
        carttickets.append(ticket)
    total= 0
    for item in session['cart']:
        total += int(float(item['price'])) * int(item['quantity'])
    reference = user.email[0:6]+ str(random.randint(1,10000))
    return render_template('web/cart.html', cart=session['cart'] ,total=total,ref=reference,user=user)



@web.route('/update_cart', methods=['POST'])
def update_cart():
    print(session['cart'])
  # Get the item and quantity from the form
    item = request.form.get('item')
    quantity = request.form.get('quantity')
    print(item)
    ind =int(item)
    print(ind)
    # Check if the user is trying to remove an item
    if request.form.get('remove'):
        # Remove the item from the cart
        del session['cart'][ind]  
    else:
        # Update the quantity of the item in the cart
        session['cart'][ind]['quantity'] = int(quantity)
        print(session['cart'])
    session.modified = True
    return redirect(url_for('web.cart'))

@web.route('/orderdetails')
def orderdetails():
    item_name = request.args.get('name')
    item_price = request.args.get('price')
    item_id = request.args.get('id')
    ticket = Ticket.query.filter(Ticket.id==item_id).first()
    print(item_name)
    return render_template('web/orderdetails.html',ticket=ticket)


@web.route("/confirmravepayment")
@login_required
def confirmravepayment():
    user = User.query.filter_by(id=session['id']).first()
    # uid = user.id
    
    if request.args.get('status') == "successful":
        transaction_id = request.args.get('transaction_id')
        # user = User.query.filter_by(email=session['email']).first()
        status = request.args.get('status')
        tx_ref = request.args.get('tx_ref')
        amount = request.args.get('amount')
        amount = int(amount)
        print(tx_ref)
        # tid = request.args.get('tid')
        tickets = request.args.get('tickets')
        print('tiick')
        cart_length=(len(session['cart']))
        # print(len(tickets)) 
        cart = Cart(total_price=amount,status=status,transaction_id=transaction_id,reference=tx_ref)
        db.session.add(cart)
        db.session.commit()
 
        cartitems = session['cart']
        print(cartitems)
        for thing in cartitems:
            print("ai")
            print(tx_ref)
            item = Item(event_id=thing['event_id'], quantity=thing['quantity'],ticket_id=thing['ticket_id'], price=thing['price'],reference=tx_ref,cart_id=0,user_id=user.id)
            db.session.add(item)
            db.session.commit()
            msg = Message(
            sender = "no-reply@3ticket.com",
            subject="Verify your email address",
            recipients=[user.email],
            html="<p>Thank you for using 3tickets. Your ticket details are below:<br>Event" + thing['eventname'] + "<br> Date:" + thing['date'] + "<br>location" + thing['location'] ,
            )
            mail.send(msg)
        session.pop('cart')            
    
        return redirect(url_for('web.cart'))
    
    
    
@web.route("/events/filter", methods=["GET", "POST"])
def filter_events():
    tags = request.args.get('tags')
    print("tags")
    print(tags)
    if request.args.get('categories'):
        print("getting categories for:")
        tags = request.args.get('tags')
        print(tags)
        x = '%{0}%'.format(tags)
            # events = Event.query.filter(and_(Event.date > datetime.date.today())).order_by(desc(Event.date)).all()

        events= Event.query.filter(Event.eventtags.like(x)).order_by(desc(Event.date)).all()
        print(events)
        return render_template("web/filter.html", events=events)
        
    if request.method == "POST":
        # Get the filter values from the form
        name = request.form.get("name")
        location = request.form.get("location")
        price_min = request.form.get("price_min")
        price_max = request.form.get("price_max")
        tags = request.form.get("tags")
        date = request.form.get("date")

        # Build the SQLAlchemy filter conditions
        conditions = []
        if name:
            # Build a list of conditions that match the name field
            # using the LIKE operator and the % wildcard
            name_conditions = [
                Event.name.like(f"%{name}%"),
                Event.name.like(f"{name}%"),
                Event.name.like(f"%{name}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the name variations
            conditions.append(or_(*name_conditions))
        if location:
            # Build a list of conditions that match the location field
            # using the LIKE operator and the % wildcard
            location_conditions = [
                Event.location.like(f"%{location}%"),
                Event.location.like(f"{location}%"),
                Event.location.like(f"%{location}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*location_conditions
            ))
            if price_min and price_max:
            # Filter for events with prices within the specified range
                conditions.append(and_(Event.baseprice >= price_min, Event.baseprice <= price_max))
            elif price_min:
            # Filter for events with prices greater than or equal to the specified minimum
                conditions.append(Event.baseprice >= price_min)
            elif price_max:
            # Filter for events with prices less than or equal to the specified maximum
                conditions.append(Event.baseprice <= price_max)
            if tags:
            # Convert the comma-separated tags string into a list of tags
                tags = tags.split(",")
            # Trim any whitespace from the tags
            tags = [tag.strip() for tag in tags]
            # Build a list of conditions that match the tags field
            # using the LIKE operator and the % wildcard
            tag_conditions = []
            for tag in tags:
                tag_conditions.append(
            Event.tags.like(f"%{tag}%"),
            Event.tags.like(f"{tag}%"),
            Event.tags.like(f"%{tag}"),
            )
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the tags
            conditions.append(or_(*tag_conditions))
            if date:
                conditions.append(Event.date == date)
            # Filter the events based on the conditions
        events = Event.query.filter(and_(*conditions)).all()
    else:
        events = []



    print (events)
# Render the events-filter.html template, passing the events as a variable
    return render_template("web/filter.html", events=events)




@web.route('/eventsschedule')
def eventsschedule():
    # events= Event.query.order_by(Event.date).all()
    events = Event.query.filter(and_(Event.date > datetime.date.today())).order_by(desc(Event.date)).all()

    
    return render_template("web/events.html",events=events)


@web.route('/allarticles')
def articles():
    articles= Article.query.all()
    
    return render_template("web/articles.html",articles=articles)

@web.route('/readarticle/<int:article_id>')
def article(article_id):
    article = Article.query.filter_by(id=article_id).first()
    title = article.title
    
    return render_template("web/article.html",article=article,title=title)


@web.context_processor
def inject_cartlength():
    about = About.query.filter_by(id=1).first()
    context = {
        "siteinfo": {
            "name": about.name,
            "number": about.number,
            "email": about.email,
            "url": "https://example.com",
            "globalcart" : len(session['cart'])
        }
    }
    # if len(session['id']) > 0:
    #     logged_in = "yes"
    # else:
    #     logged_in = "no"
    return dict(globalcart=len(session['cart']))


@web.context_processor
def inject_about():
    about = About.query.filter_by(id=1).first()
    return dict(siteabout=about)