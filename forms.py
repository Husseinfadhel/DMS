from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL, Length


class AddClient(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    phone = StringField("phone", validators=[DataRequired()])
    address = StringField("address", validators=[DataRequired()])


class Search(FlaskForm):
    search = StringField('search')
