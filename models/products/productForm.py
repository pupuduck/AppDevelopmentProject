from wtforms import StringField, validators, DecimalField, FileField, SubmitField, IntegerField, IntegerRangeField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_wtf import FlaskForm


class CreateProductForm(FlaskForm):
    Name = StringField("Product name", [validators.length(min=1, max=150), validators.DataRequired()])
    Rating = StringField('Rating out of 5', [validators.Length(min=1, max=5), validators.DataRequired()])
    Description = StringField('Product description', [validators.DataRequired()])
    Price = DecimalField('Price of product', [validators.DataRequired()], places=2)
    Image = FileField('Image of product', [validators.DataRequired()])
    Submit = SubmitField()


class AddToCart(FlaskForm):
    Quantity = IntegerField('Quantity', validators=[DataRequired()])

