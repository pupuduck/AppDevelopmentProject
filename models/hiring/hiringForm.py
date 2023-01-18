from wtforms import Form, StringField, RadioField, SelectField, TextAreaField, validators,IntegerField,FileField
from wtforms.fields import EmailField, DateField


class CreateResumesForm(Form):
    first_name = StringField('First Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    email = EmailField('Email', [validators.Email(), validators.DataRequired()])
    address = TextAreaField('Mailing Address', [ validators.DataRequired()])
    sgorpr = RadioField('Are you a Singaporean or Singapore PR', choices=[('Yes', 'Yes'), ('No', 'No')], default='Yes')
    citizenship = SelectField('Citizenship', choices=[('Singaporean', 'Singaporean'), ('Singapore PR', 'Singapore PR')],
                              default='Singaporean')
    preferredjob = SelectField('Position that you are applying for ',
                                   choices=[('Service Crew (Full-Time)', 'Service Crew (Full-Time)'),
                                            ('Service Crew (Part-Time)', 'Service Crew (Part-Time)'), (
                                            'Night Shift Kitchen Crew (Part-time)',
                                            'Night Shift Kitchen Crew (Part-time)'),
                                            ('Washer (Part-time)', 'Washer (Part-time)'),
                                            ('Driver (Full-Time)', 'Driver (Full-Time)'), (
                                            'Assistant Outlet Manager (Full-Time)',
                                            'Assistant Outlet Manager (Full-Time)'),
                                            ('Assistant Supervisor (Full-Time)', 'Assistant Supervisor (Full-Time)')],
                                   default='Service Crew (Full-Time)')
    contactno = IntegerField('Primary Contact Number', [validators.NumberRange(min=10000000,max=99999999),validators.DataRequired()])
    uploadfile = FileField('Upload your resume here',[ validators.DataRequired()])


class CreateJobPositionsForm(Form):
    jobname = StringField('What is the name of the job?', [validators.Length(min=1, max=150), validators.DataRequired()])
    jobavailability = SelectField('Is there availability for the job now?', choices=[('Available', 'Available'), ('Not Available', 'Not Available')],
                              default='Available')
    jobrequirements = StringField('What are the requirements of the job?', [ validators.DataRequired()])
    jobresponsibility = StringField('What are the responsibilities of the job?', [ validators.DataRequired()])
    jobsalary = StringField('What is the salary of the job', [ validators.DataRequired()])

