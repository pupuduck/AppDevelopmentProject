from wtforms import StringField, EmailField, PasswordField, SubmitField, IntegerField, DateField, FileField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=5, max=15), DataRequired()])
    email = EmailField('Email', validators=[Email(), DataRequired()])
    password1 = PasswordField('Password', validators=[Length(min=8), DataRequired()])
    password2 = PasswordField('Confirm password', validators=[Length(min=8), EqualTo('password1', message="Passwords must be the same"), DataRequired()])
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=5, max=15), DataRequired()])
    password = PasswordField('Password', validators=[Length(min=8), DataRequired()])
    submit = SubmitField('Log in')


class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=5, max=15), DataRequired()])
    location = StringField('Location')
    email = EmailField('Email', validators=[Email(), DataRequired()])
    phone = IntegerField('Phone number', validators=[Length(8)])
    birthday = DateField('Birthday')
    image = FileField()
    submit1 = SubmitField('Save Changes')


class UpdatePasswordForm(FlaskForm):
    password1 = PasswordField('Enter current password', validators=[DataRequired()])
    password2 = PasswordField('Enter new password', validators=[DataRequired(), Length(min=8), EqualTo('password3', message="Passwords must be the same")])
    password3 = PasswordField('Re-enter new password', validators=[DataRequired(), Length(min=8), EqualTo('password2', message="Passwords must be the same")])
    submit2 = SubmitField('Save Changes')


class CreditCardForm(FlaskForm):
    full_name = StringField('Cardholder name: ', validators=[DataRequired()])
    card_number = StringField('Card number: ', validators=[DataRequired(), Length(16)])
    cvv = StringField('CVV: ', validators=[Length(3)])
    expiry_month = SelectField('Expiry Month: ', choices=[(1, '01'), (2, '02'), (3, '03'), (4, '04'), (5, '05'),
                                                          (6, '06'), (7, '07'), (8, '08'), (9, '09'), (10, '10'),
                                                          (11, '11'), (12, '12')])
    expiry_year = SelectField('Expiry Year: ', choices=[(23, '23'), (24, '24'), (25, '25'), (26, '26'), (27, '27'),
                                                        (28, '28'), (29, '29'), (30, '30'), (31, '31'), (32, '32'),
                                                        (33, '33'), (34, '34')])


