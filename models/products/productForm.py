from wtforms import StringField, validators, DecimalField, FileField, SubmitField
from flask_wtf import FlaskForm


class CreateProductForm(FlaskForm):
    Name = StringField("Product name", [validators.length(min=1, max=150), validators.DataRequired()])
    Rating = StringField('Rating out of 5', [validators.Length(min=1, max=5), validators.DataRequired()])
    Description = StringField('Product description', [validators.DataRequired()])
    Price = DecimalField('Price of product', [validators.DataRequired()], places=2)
    Image = FileField('Image of product', [validators.DataRequired()])
    Submit = SubmitField()
    # product = StringField('Product name', [validators.Length(min=1, max=150), validators.DataRequired()])
    # code = StringField('code', [validators.Length(min=8, max=8), validators.DataRequired()])
    # nutritional = SelectField('nutritional grade', [validators.DataRequired()], choices=[('', 'Select'),
    # ('A', 'Very healthy'), ('B', 'healthy'), ('c', 'Un-healthy')], default='')
    # price = DecimalField('price', [validators.DataRequired()], places=2)


