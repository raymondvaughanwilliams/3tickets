from flask import render_template,request,Blueprint,redirect,url_for,session,current_app
from structure.models import User ,WebFeature,Event , Ticket ,Article
from structure import db,photos
from structure.core.forms import AddEvent,AddTicket,AddArticle
from sqlalchemy.orm import load_only
from flask_login import login_required
import secrets
import os


web = Blueprint('web',__name__)


@web.route('/homepage')
def homepage():
    '''
    This is the home page view. Notice how it uses pagination to show a limited
    number of posts by limiting its query size and then calling paginate.
    '''
    page = request.args.get('page', 1, type=int)
    events = Event.query.all()
    articles = Article.query.all()
    web_features = WebFeature.query.order_by(WebFeature.date.desc()).paginate(page=page, per_page=10)
    return render_template('web/homepage.html',web_features=web_features,events=events,articles=articles)