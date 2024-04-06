from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, DecimalField, SelectField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, Email, ValidationError
    
# Add Special Character Validator (Command Injection Protection)
def disallowed_characters(form, field):
    disallowed_chars = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+', '=', '/', '\\', '|', '`', '~', '<', '>', '[', ']', '{', '}', ';', ':', ',', '.', '?', "'", '"']
    for char in field.data:
        if char in disallowed_chars:
            raise ValidationError(f'Special characters are not allowed: {char}')

class NewListingForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=4, max=20), disallowed_characters])
    description = StringField('Description', validators=[DataRequired(), Length(min=20, max=50), disallowed_characters])
    image = FileField('Image', validators=[DataRequired(), FileAllowed(['jpg', 'png'], 'Images Only!')])
    price = DecimalField('Price', validators=[DataRequired()])

class NewUserForm(FlaskForm):
    user_type = SelectField('Buyer or Seller?', choices=['Buyer', 'Seller'], validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=10), disallowed_characters])
    password = PasswordField('Password')
    confirm_password= PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message="Passwords Must Match")
    ])
    first_name = StringField('First Name', validators=[DataRequired(), disallowed_characters])
    last_name = StringField('Last Name', validators=[DataRequired(), disallowed_characters])
    email = StringField('Email', validators=[DataRequired(), Email()])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), disallowed_characters])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])

class ContactForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), disallowed_characters])
    last_name = StringField('Last Name', validators=[DataRequired(), disallowed_characters])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired(), disallowed_characters])

class NewPasswordForm(FlaskForm):
    old_password = PasswordField('Previous Password', validators=[
        DataRequired()
    ])
    new_password = PasswordField('New Password', validators=[
        DataRequired()
    ])