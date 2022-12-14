import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from sqlalchemy import MetaData
from jinja2 import Environment, select_autoescape
from dotenv import load_dotenv

load_dotenv()



app = Flask(__name__)


app.config['SECRET_KEY'] = 'asecretkey'
############################
### DATABASE SETUP ##########
########################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(app,metadata=MetaData(naming_convention=naming_convention))
Migrate(app,db)
migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername == "sqlite":
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)


app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images/events')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# patch_request_class(app)


app.config.update(
    UPLOAD_PATH = os.path.join(basedir, 'static')
)

#########################
# LOGIN CONFIGS
login_manager = LoginManager()

login_manager.init_app(app)
login_manager.login_view = 'users.login'



def split(value, separator):
    return value.split(separator)

@app.before_request
def add_filters():
    app.jinja_env.filters['split'] = split
    
    
emailpassword = os.environ.get('MAIL_PASSWORD')
print(emailpassword)


##################################################


from structure.core.views import core
from structure.users.views import users
from structure.userportal.views import userportal
from structure.web.views import web
from structure.error_pages.handlers import error_pages


app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(error_pages)
app.register_blueprint(web)
app.register_blueprint(userportal)

