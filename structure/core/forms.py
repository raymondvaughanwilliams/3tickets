from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, validators , ValidationError, HiddenField,FloatField,IntegerField,SubmitField,SelectField,SelectMultipleField,TextAreaField,FileField,Form,DateTimeField,TimeField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed,FileRequired
from wtforms_components import TimeField
from wtforms.fields.html5 import DateField
import datetime
from flask_login import current_user
from structure.models import User


class AddEvent(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    location = StringField('Location',validators=[])
    date = DateField('Choose Date', [validators.DataRequired()] )
    description = StringField('Description')
    days = StringField('Days')
    number = StringField('Number')
    email = StringField('Email',validators=[DataRequired(),Email()])
    tags = StringField('Tags')
    baseprice = IntegerField('Lowest Price.Enter 0 if event is free',validators=[DataRequired()])
    time  = TimeField('Time',default=datetime.datetime.now)
    image1 = FileField('Image 1', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    image2 = FileField('Image 2', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    image3 = FileField('Image 3', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    submit = SubmitField('Submit')
    
    
class AddTicket(FlaskForm):
    name = StringField('Name',validators=[DataRequired()])
    day = StringField('Day',validators=[])
    quantity = IntegerField('Quantity',validators=[])
    price = FloatField('Price',validators=[])
    features = StringField('Features')
    image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])

    submit = SubmitField('Submit')
    
    
class AddArticle(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    content = StringField('Content',validators=[])
    image = FileField('Image', validators=[FileRequired(), FileAllowed(['jpg','png','gif','jpeg'])])
    submit = SubmitField('Submit')