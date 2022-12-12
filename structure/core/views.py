from flask import render_template,request,Blueprint,redirect,url_for,session,current_app
from structure.models import User ,WebFeature,Event , Ticket ,Article
from structure import db,photos
from structure.core.forms import AddEvent,AddTicket,AddArticle
from sqlalchemy.orm import load_only
from flask_login import login_required
import secrets
import os
import datetime
core = Blueprint('core',__name__)




allowed_extensions = ['png', 'jpg', 'jpeg', 'gif','mp4']
def check_file_extension(filename):
    return filename.rsplit('.', 1)[1].lower() in allowed_extensions






@core.route('/')
@login_required
def index():
    '''
    This is the home page view. Notice how it uses pagination to show a limited
    number of posts by limiting its query size and then calling paginate.
    '''
    page = request.args.get('page', 1, type=int)
    events = Event.query.all()
    articles = Article.query.all()
    web_features = WebFeature.query.order_by(WebFeature.date.desc()).paginate(page=page, per_page=10)
    return render_template('index.html',web_features=web_features,events=events,articles=articles)

@core.route('/base')
def base():
    '''
    Example view of any other "core" page. Such as a info page, about page,
    contact page. Any page that doesn't really sync with one of the models.
    '''
    return render_template('base.html')



# All events
@core.route('/events')
def events():
    events = Event.query.all()
    return render_template('events/events.html',events=events)


# Add event 
@core.route('/addevent',methods=['GET', 'POST'])
def addevent():
    events = Event.query.all()
    '''
    Example view of any other "core" page. Such as a info page, about page,
    contact page. Any page that doesn't really sync with one of the models.
    '''
    # user_id = session['id']
    # print(user_id)
    form = AddEvent()
    #process data and save it to db 
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
        
        print('date')
        print(date)
        print(name)
        
        # Get the current date and time
        now = datetime.date.today()

        # Check if the date has passed
        if date < now:
            status = "passed"
        else:
            status = "pending"

        # Print the result
        print(status)

        
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

        event = Event(name=name,date=date,time=time,location=location,description=description,days=days,email=email,number=number,image1=image1,image2=image2,image3=image3,eventtags=tags,baseprice=baseprice,user_id=session['id'],status=status)
        db.session.add(event)
        db.session.commit()
        # flash(f'Meme added successfully','success')
        return redirect(url_for('core.index'))


    return render_template('events/addevent.html',events=events,form=form)




# Edit Event
@core.route('/editevent/<int:event_id>', methods=['GET', 'POST'])
@login_required
def editevent(event_id):
    event = Event.query.get_or_404(event_id)


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
        if request.files.get('image1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/events/" + event.image_1))
                image1 = photos.save(request.files.get('image1'), name=secrets.token_hex(10) + ".")
                event.image1 = "static/images/events/"+image1
            except:
                image1 = photos.save(request.files.get('image1'), name=secrets.token_hex(10) + ".")
                event.image1 = "static/images/events/"+image1
        db.session.commit() 
        print('updated')
        return redirect(url_for('core.addevent'))

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
    return render_template('events/editevent.html', form=form,event=event)


# An Event
@core.route('/event/<int:event_id>')
@login_required
def event(event_id):
    user = User.query.filter_by(email=session['email']).first()

    event = Event.query.filter_by(event_id=event_id).first()
    return render_template('event.html', event=event,user=user)



# Delete Event
@core.route("/delete_event/<int:event_id>", methods=['POST','GET'])
@login_required
def delete_event(event_id):
    events = Event.query.filter_by(phonebook_id=event_id).all()
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    # for contact in contacts:
    #     db.session.delete(contact)
    #     db.session.commit()


    # flash('Post has been deleted')
    return redirect(url_for('core.index'))














# All tickets
@core.route('/tickets')
def tickets():
    tickets = Ticket.query.all()
    return render_template('tickets/tickets.html',tickets=tickets)



# Add event 
@core.route('/addticket/<int:event_id>',methods=['GET', 'POST'])
def addticket(event_id):
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
        return redirect(url_for('core.index'))


    return render_template('tickets/addticket.html',tickets=tickets,form=form)




# Edit ticket
@core.route('/editticket/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def editticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)


    form = AddTicket()
    if request.method == 'POST':     
        ticket.price = form.price.data
        ticket.day = form.day.data
        ticket.quantity = form.quantity.data
        ticket.name = form.name.data
        ticket.features = form.features.data
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
        form.features.data = ticket.features
    return render_template('tickets/editticket.html', form=form,ticket=ticket)


# An ticket
@core.route('/ticket/<int:ticket_id>')
@login_required
def ticket(ticket_id):
    user = User.query.filter_by(email=session['email']).first()
    ticket = Ticket.query.filter_by(ticket_id=ticket_id).first()
    return render_template('tickets/ticket.html', ticket=ticket,user=user)


# Delete ticket
@core.route("/delete_ticket/<int:ticket_id>", methods=['POST','GET'])
@login_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    # for contact in contacts:
    #     db.session.delete(contact)
    #     db.session.commit()


    # flash('Post has been deleted')
    return redirect(url_for('core.index'))





# All articles
@core.route('/articles')
def articles():
    articles = Article.query.all()
    return render_template('articles/articles.html',articles=articles)

# Add article 
@core.route('/addarticle',methods=['GET', 'POST'])
def addarticle():
    articles = Article.query.all()
    form = AddArticle()
    #process data and save it to db 
    if request.method == 'POST' :
        # name = form.name.data
        title = form.title.data
        content = form.content.data
        if request.files.get('image'):
            image = photos.save(request.files['image'], name=secrets.token_hex(10) + ".")
            image= "static/images/events/"+image
        else:
            image = "static/images/noimage.JPG"
        # image = photos.save(request.files['image'], name=secrets.token_hex(10) + ".")
        # image= "static/images/events/"+image
        article = Article(title=title, content=content,image=image)
        db.session.add(article)
        db.session.commit()
        # flash(f'Meme added successfully','success')
        return redirect(url_for('core.index'))


    return render_template('articles/addarticle.html',articles=articles,form=form)




# Edit article
@core.route('/editarticle/<int:article_id>', methods=['GET', 'POST'])
@login_required
def editarticle(article_id):
    article = Article.query.get_or_404(article_id)


    form = AddArticle()
    if request.method == 'POST':     
        article.title = form.title.data
        article.content = form.content.data
        if request.files.get('image'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/articles/" + article.image_1))
                image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + ".")
                article.image = "static/images/events/"+image
            except:
                image = photos.save(request.files.get('image'), name=secrets.token_hex(10) + ".")
                article.image = "static/images/events/"+image
        db.session.commit() 
        print('updated')
        return redirect(url_for('core.index'))

    elif request.method == 'GET':
        form.title.data = article.title
        form.content.data = article.content
    return render_template('articles/editarticle.html', form=form,article=article)


# An article
@core.route('/article/<int:article_id>')
@login_required
def article(article_id):
    user = User.query.filter_by(email=session['email']).first()
    article = Article.query.filter_by(article_id=article_id).first()
    return render_template('articles/article.html', article=article,user=user)


# Delete article
@core.route("/delete_article/<int:article_id>", methods=['POST','GET'])
@login_required
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()


    # flash('Post has been deleted')
    return redirect(url_for('core.index'))










# @core.route('/add-to-cart/<event_id>')
# def add_to_cart(event_id):
#     # Retrieve the details of the selected ticket from the database
#     event = Event.objects.get(id=event_id)
#     ticket = event.tickets.get(id=request.args.get('ticket_id'))
    
#     # Check if the user is logged in
#     if not current_user.is_authenticated:
#         flash('Please log in or create an account to purchase tickets.')
#         return redirect(url_for('login'))
    
#     # Check if the user already has a shopping cart
#     if not hasattr(current_user, 'shopping_cart'):
#         current_user.shopping_cart = ShoppingCart()
    
#     # Add the selected ticket to the user's shopping cart
#     current_user.shopping_cart.add_ticket(ticket)
    
#     # Update the total cost of the shopping cart
#     current_user.shopping_cart.update_total()
    
#     # Save the updated shopping cart to the database
#     current_user.save()
    
#     flash('Ticket added to shopping cart.')
#     return redirect(url_for('view_cart'))


# GUESTLIST MANAGEMENT
# LINK.TO 
# Allow hosts send mails to attendees