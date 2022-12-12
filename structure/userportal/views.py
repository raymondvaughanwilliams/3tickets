from flask import render_template,request,Blueprint,redirect,url_for,session,current_app
from structure.models import User ,WebFeature,Event , Ticket ,Article ,NewsletterEmails ,Newsletter ,About, Cart,Item
from structure import db,app,photos 
from structure.web.forms import NewsletterSubForm 
from structure.core.forms import AddEvent, AddTicket 
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
    tickets_length = len(tickets)
    print(tickets)
    mytickets = []
    # if tickets:
    for ticket in tickets:
        print(ticket.tickets)
    events = Event.query.limit(4)
    #     tick = Ticket.query.filter_by(id=ticket.ticket_id).first()
    #     print(tick.event)
    #     mytickets.append({'name': tick.name, 'price': tick.price,'ticket_id':tick.id,'eventname':tick.event.name,'location':tick.event.location,'date':tick.event.date,'quantity':1,'image':tick.image,'event_id':tick.event_id})   
    # print(mytickets)
    return render_template('userportal/mytickets.html',tickets = tickets,events=events,tickets_length=tickets_length)



@userportal.route("/hostedevents", methods=['POST','GET'])
@login_required
def hostedevents():
    events = Event.query.filter(Event.user_id == session['id']).all()
    about = About.query.filter_by(id=1).first()
    return render_template('userportal/hostedevents.html',about = about,events=events)



@userportal.route('/hostevent',methods=['GET', 'POST'])
def hostevent():
    form  =AddEvent()
    if request.method == 'POST' :
        name = form.name.data
        date = form.date.data
        time = form.time.data
        location = form.location.data
        description = form.description.data
        days = form.days.data
        email = form.email.data
        number = form.number.data
        tags = form.tags.data
        baseprice = form.baseprice.data
        if request.files.get('image1'):
            image1 = photos.save(request.files['image1'], name=secrets.token_hex(10) + ".")
            image1= "static/images/events/"+image1
        else:
            image1 = "static/images/noimage.JPG"      
        # image_1 = photos.save(request.files['image1'], name=secrets.token_hex(10) + ".")
        # image1= "static/images/events/"+image_1
        image_2 = photos.save(request.files['image2'], name=secrets.token_hex(10) + ".")
        image2= "static/images/events/"+image_2
        image_3 = photos.save(request.files['image3'], name=secrets.token_hex(10) + ".")
        image3= "static/images/events/"+image_3

        
        # Get the current date and time
        now = datetime.date.today()

        # Check if the date has passed
        if date < now:
            status = "passed"
        else:
            status = "pending"

        # Print the result
        print(status)
        event = Event(name=name,date=date,time=time,location=location,description=description,days=days,email=email,number=number,image1=image1,image2=image2,image3=image3,eventtags=tags,baseprice=baseprice,status=status)
        db.session.add(event)
        db.session.commit()
        # flash(f'Meme added successfully','success')
        return redirect(url_for('web.homepage'))

    return render_template('userportal/addevent.html',form=form)



@userportal.route('/editmyevent/<int:event_id>', methods=['GET', 'POST'])
@login_required
def editmyevent(event_id):
    event = Event.query.get_or_404(event_id)
    if event.user_id == session['id']:


        form = AddEvent()
        if request.method == 'POST':     
            event.name = form.name.data
            event.date = form.date.data
            event.time = form.time.data
            event.description = form.description.data
            event.location = form.location.data
            event.days = form.days.data
            event.number = form.number.data
            event.email = form.email.data
            event.baseprice = form.baseprice.data
            # if request.files.get('image1'):
            #     try:
            #         os.unlink(os.path.join(current_app.root_path, "static/images/events/" + event.image_1))
            #         image1 = photos.save(request.files.get('image1'), name=secrets.token_hex(10) + ".")
            #         event.image1 = "static/images/events/"+image1
            #     except:
            #         image1 = photos.save(request.files.get('image1'), name=secrets.token_hex(10) + ".")
            #         event.image1 = "static/images/events/"+image1
            db.session.commit() 
            print('updated')
            return redirect(url_for('web.homepage'))

        elif request.method == 'GET':
            form.name.data = event.name
            form.date.data = event.date
            form.time.data = event.time
            form.description.data = event.description
            form.location.data = event.location
            form.days.data = event.days
            form.number.data = event.number
            form.email.data = event.email
            form.baseprice.data = event.baseprice
  
    else:
        return redirect(url_for('userportal.not_allowed'))
    return render_template('userportal/editevent.html', form=form,event=event)


# An Event
@userportal.route('/myevent/<int:event_id>')
@login_required
def event(event_id):
    user = User.query.filter_by(id=session['id']).first()
    tickets = Ticket.query.filter(Ticket.event_id == event_id).all()
    event = Event.query.filter_by(id=event_id).first()
    return render_template('userportal/event.html', event=event,user=user,tickets=tickets)



# Delete Event
@userportal.route("/delete_myevent/<int:event_id>", methods=['POST','GET'])
@login_required
def delete_myevent(event_id):
    events = Event.query.filter_by(phonebook_id=event_id).all()
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    # for contact in contacts:
    #     db.session.delete(contact)
    #     db.session.commit()


    # flash('Post has been deleted')
    return redirect(url_for('core.index'))



@userportal.route('/tickets')
def tickets():
    tickets = Ticket.query.all()
    return render_template('tickets/tickets.html',tickets=tickets)



# Add event 
@userportal.route('/addmyticket/<int:event_id>',methods=['GET', 'POST'])
def addmyticket(event_id):
    # if ticket.event.user_id == session['id']:
    tickets = Ticket.query.all()
    '''
    Example view of any other "core" page. Such as a info page, about page,
    contact page. Any page that doesn't really sync with one of the models.
    '''
    user_id = session['id']
    print(user_id)
    form = AddTicket()
    #process data and save it to db 
    if request.method == 'POST' :
        # name = form.name.data
        price = form.price.data
        day = form.day.data
        quantity = form.quantity.data
        name = form.name.data
        features = form.features.data
        if request.files.get('image'):
            image = photos.save(request.files['image'], name=secrets.token_hex(10) + ".")
            image= "static/images/events/"+image
        else:
            image = "static/images/noimage.JPG"
       


        # image_1 = photos.save(request.files['image_1'], name=secrets.token_hex(10) + ".")
        # img= "/static/images/events/"+image_1
        #check file format 
        # if check_file_extension(image_1):
        ticket = Ticket(day=day,price=price,quantity=quantity,event_id=event_id,name=name,image=image,features=features)
        db.session.add(ticket)
        db.session.commit()
        # flash(f'Meme added successfully','success')
        return redirect(url_for('web.homepage'))


    return render_template('userportal/addticket.html',tickets=tickets,form=form)




# Edit ticket
@userportal.route('/editmyticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def editticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)


    form = AddTicket()
    if request.method == 'POST':     
        ticket.price = form.price.data
        ticket.day = form.day.data
        ticket.quantity = form.quantity.data
        ticket.name = form.name.data
        if request.files.get('image'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/tickets/" + ticket.image_1))
                image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + ".")
                ticket.image = "static/images/events/"+image
            except:
                image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + ".")
                ticket.image = "static/images/events/"+image
        db.session.commit() 
        print('updated')
        return redirect(url_for('core.index'))

    elif request.method == 'GET':
        form.price.data = ticket.price
        form.quantity.data = ticket.quantity
        form.day.data = ticket.day
        form.name.data = ticket.name
    return render_template('userportal/editticket.html', form=form,ticket=ticket)


# An ticket
@userportal.route('/ticket/<int:ticket_id>')
@login_required
def ticket(ticket_id):
    user = User.query.filter_by(id=session['id']).first()
    ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
    return render_template('userportal/ticket.html', ticket=ticket,user=user)


# Delete ticket
@userportal.route("/delete_ticket/<int:ticket_id>", methods=['POST','GET'])
@login_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    # for contact in contacts:
    #     db.session.delete(contact)
    #     db.session.commit()


    # flash('Post has been deleted')
    return redirect(url_for('web.homepage'))



@userportal.route("/not-allowed")
def not_allowed():
    test = "test"
    return render_template('userportal/notallowed.html',test=test)