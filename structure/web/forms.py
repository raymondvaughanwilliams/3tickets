from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, validators , ValidationError, HiddenField,FloatField,IntegerField,SubmitField,SelectField,SelectMultipleField,TextAreaField,FileField,Form,DateTimeField,TimeField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed,FileRequired
from wtforms_components import TimeField
from wtforms.fields.html5 import DateField,DateTimeField
import datetime
from flask_login import current_user
from structure.models import User


    
    
class NewsletterSubForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    submit = SubmitField('Subscribe')