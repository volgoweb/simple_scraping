from wtforms import StringField, Form
from wtforms.validators import Email
from wtforms.widgets import PasswordInput


class LoginForm(Form):
    email = StringField('Email', validators=[Email()])
    password = StringField('Password', widget=PasswordInput())
