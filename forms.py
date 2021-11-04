from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL, Length


class AddClient(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    phone = StringField("phone", validators=[DataRequired()])
    address = StringField("address", validators=[DataRequired()])


class Search(FlaskForm):
    search = StringField('search')


class AddDriver(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    phone = StringField("phone", validators=[DataRequired()])
    card_no = StringField("card_no", validators=[DataRequired()])


class AddMasrf(FlaskForm):
    reason = StringField("name", validators=[DataRequired()])
    amount = StringField("phone", validators=[DataRequired()])


class AddOrder(FlaskForm):
    invoice_num = StringField(validators=[DataRequired()])
    total = StringField(validators=[DataRequired()])
    net = StringField(validators=[DataRequired()])