from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators


class CreateReportForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    gender = SelectField('Gender', [validators.DataRequired()], choices=[('', 'Select'), ('F', 'Female'), ('M', 'Male')], default='')
    membership = RadioField('Position', choices=[('W', 'Worker'), ('M', 'Manager'), ('H', 'Head')], default='W')
    remarks = TextAreaField('Enter the donut type sold:', [validators.Optional()])
