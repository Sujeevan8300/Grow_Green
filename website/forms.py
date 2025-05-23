from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, EmailField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, length, NumberRange, Length
from flask_wtf.file import FileField, FileRequired
from .models import Category


class SignUpForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), length(min=2)])
    password1 = PasswordField('Enter Your Password', validators=[DataRequired(), length(min=6)])
    password2 = PasswordField('Confirm Your Password', validators=[DataRequired(), length(min=6)])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Enter Your Password', validators=[DataRequired()])
    submit = SubmitField('Log in')


class PasswordChangeForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired(), length(min=6)])
    new_password = PasswordField('New Password', validators=[DataRequired(), length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), length(min=6)])
    change_password = SubmitField('Change Password')



# class ShopItemsForm(FlaskForm):
    # product_name = StringField('Name of Product', validators=[DataRequired()])
    #current_price = FloatField('Current Price', validators=[DataRequired()])
    #previous_price = FloatField('Previous Price', validators=[DataRequired()])
    #in_stock = IntegerField('In Stock', validators=[DataRequired(), NumberRange(min=0)])
    #product_picture = FileField('Product Picture', validators=[FileRequired()])
    #flash_sale = BooleanField('Flash Sale')

    #add_product = SubmitField('Add Product')
    #update_product = SubmitField('Update')

class ShopItemsForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired()])
    previous_price = FloatField('Previous Price', validators=[DataRequired()])
    current_price = FloatField('Current Price', validators=[DataRequired()])
    in_stock = IntegerField('In Stock', validators=[DataRequired()])
    product_picture = FileField('Product Picture', validators=[FileRequired()])
    flash_sale = BooleanField('Flash Sale')
    
    # Add category selection field
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])

    submit = SubmitField('Add Product')



class OrderForm(FlaskForm):
    order_status = SelectField('Order Status', choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'),
                                                        ('Out for delivery', 'Out for delivery'),
                                                        ('Delivered', 'Delivered'), ('Canceled', 'Canceled')])

    update = SubmitField('Update Status')



class DeliveryAddressForm(FlaskForm):
    """Form for handling delivery addresses during order placement."""
    delivery_address = TextAreaField('Delivery Address', validators=[DataRequired(), Length(min=4, max=500)])
    submit = SubmitField('Place Order')



class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Length(max=300)])
    submit = SubmitField('Save')