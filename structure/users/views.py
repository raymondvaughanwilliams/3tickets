# users/views.py
from flask import render_template,url_for,flash,redirect,request,Blueprint,session
from flask_login import login_user, current_user, logout_user, login_required
from structure import db,app
from structure.models import User, WebFeature
from structure.users.forms import RegistrationForm,LoginForm,UpdateUserForm
from structure.users.picture_handler import add_profile_pic
from flask_mail import Message,Mail
import random

users = Blueprint('users',__name__)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "raymondvaughanwilliams@gmail.com"
app.config["MAIL_PASSWORD"] = "fwlxpuuiqvjwcxoz"

mail = Mail(app)

def send_verification_email():
    # Get the email address from the request
    email = request.form["email"]

    # Create the message
    msg = Message(
        subject="Verify your email address",
        recipients=[email],
        html="<p>Thank you for signing up. Please click the following link to verify your email address:</p><p><a href='http://www.example.com/verify?verification_code={}'>http://www.example.com/verify?verification_code={}</a></p>".format( request.form["email"],  request.form["email"]),
    )
# register
@users.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    

    if form.validate_on_submit():
        vcode  = form.email.data[0:6]+ str(random.randint(1,10000)) 
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,verification_code=vcode,role="user",name=form.name.data,
                    verification="no")

        db.session.add(user)
        db.session.commit()
        msg = Message(
        sender = "no-reply@3ticket.com",
        subject="Ticket Details",
        recipients=[form.email.data],
        html="<p>Thank you for signing up. Please click the following link to verify your email address:</p><p><a href='http://127.0.0.1:5000/accountverification?verification_code={}'>http://127.0.0.1:5000/accountverification?verification_code={}</a></p>".format( vcode,  vcode),
        )
        mail.send(msg)
        
        flash('Thanks for registration!')
        return redirect(url_for('users.login'))

    return render_template('register2.html',form=form)




@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()
        session['id'] = user.id
        # session['role'] = user.role

        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user.check_password(form.password.data) and user is not None:
            #Log in the user
            if user.verification == "no":
                return redirect(url_for('users.verifyaccount'))
            
            login_user(user)
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('core.index')

            return redirect(next)
    return render_template('login2.html', form=form)

# logout
@users.route("/logout")
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("web.homepage"))


@users.route("/verify-account")
def verify_account():
    form = RegistrationForm()
    if request.method == 'POST':
        email = form.email.data

        vcode  = str(random.randint(1,10000)) 
        msg = Message(
        sender = "no-reply@3ticket.com",
        subject="Ticket Details",
        recipients=[form.email.data],
        html="<p>Thank you for signing up. Please click the following link to verify your email address:</p><p><a href='http://127.0.0.1:5000/accountverification?verification_code={}'>http://127.0.0.1:5000/accountverification?verification_code={}</a></p>".format( vcode,  vcode),
        )
        mail.send(msg)
    

    return render_template('web/verify.html',form=form)
    
    

@users.route("/accountverification")
def account_verification():
    verification_code = request.args.get('verification_code')
    user = User.query.filter_by(verification_code=verification_code).first()
    
    user.verification = "yes"
    db.session.commit()
    return redirect(url_for('users.login'))
    
    
    
    
    
# account (update UserForm)
# @users.route("/account", methods=['GET', 'POST'])
# @login_required
# def account():

#     form = UpdateUserForm()

#     if form.validate_on_submit():

#         if form.picture.data:
#             username = current_user.username
#             pic = add_profile_pic(form.picture.data,username)
#             current_user.profile_image = pic

#         current_user.username = form.username.data
#         current_user.email = form.email.data
#         db.session.commit()
#         flash('User Account Updated')
#         return redirect(url_for('users.account'))

#     elif request.method == 'GET':
#         form.username.data = current_user.username
#         form.email.data = current_user.email

#     profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
#     return render_template('account.html', profile_image=profile_image, form=form)

# @users.route("/<username>")
# def user_posts(username):
#     page = request.args.get('page',1,type=int)
#     user = User.query.filter_by(username=username).first_or_404()
#     web_features = WebFeature.query.filter_by(author=user).order_by(WebFeature.date.desc()).paginate(page=page,per_page=5)
#     return render_template('user_web_features.html',web_features=web_features,user=user)

















# user's list of Blog posts
