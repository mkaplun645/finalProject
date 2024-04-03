from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, DecimalField, SelectField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, Regexp, EqualTo, Email, ValidationError
from blacklist import EASILY_GUESSABLE_PASSWORDS

# API (Application Programming Interface) - Collection of Endpoints that We Can Interact With
    # External Apis
        # Google Maps (GeoLocation)
        # Amazon (Display Similar Products / Listings)
            # User types in a Product
            # That string is sent to the Amazon API, which returns a list of matching products
            # Render the list of matching products to our application
    # Internal APIs
        # Flask Application (Routes)

# Add Custom Password Validator
def not_easily_guessable_password(form, field):
    if field.data in EASILY_GUESSABLE_PASSWORDS:
        raise ValidationError('Easily Guessable Password.')
    
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
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=5, message="Password must be at least 5 characters long."),
        Regexp(regex=r'^(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$', message="Password must contain at least one special character."),
        not_easily_guessable_password
    ])
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
        DataRequired(),
        Length(min=5, message="Password must be at least 5 characters long."),
        Regexp(regex=r'^(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$', message="Password must contain at least one special character.")
    ])

class ContactForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), disallowed_characters])
    last_name = StringField('Last Name', validators=[DataRequired(), disallowed_characters])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired(), disallowed_characters])

class NewPasswordForm(FlaskForm):
    old_password = PasswordField('Previous Password', validators=[
        DataRequired(),
        Length(min=5, message="Password must be at least 5 characters long."),
        Regexp(regex=r'^(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$', message="Password must contain at least one special character.")
    ])
    new_password = PasswordField('New Password', validators=[
        DataRequired(), 
        Length(min=5, message="Password must be at least 5 characters long."),
        Regexp(regex=r'^(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$', message="Password must contain at least one special character.")
    ])