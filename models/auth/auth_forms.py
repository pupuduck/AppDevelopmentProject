from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=5, max=15), DataRequired()])
    email = EmailField('Email', validators=[Email()])
    password1 = PasswordField('Password', validators=[Length(min=8)])
    password2 = PasswordField('Confirm password', validators=[Length(min=8), EqualTo(password1)])
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=5, max=15), DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8)])
    submit = SubmitField('Log in')
