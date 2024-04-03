from models import User, Contact, Listing, db
from app import create_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, user_logged_in
from flask import Flask
import pymysql

pymysql.install_as_MySQLdb()

# Example:

# def func(x):
#     return x + 1

# def test_answer():
#     assert func(4) == 5

# Class (Unit) Tests - Attribute Setters / Getters

# Instance Tests - Instance Methods

# End-to-End Tests

# A User can log in
# A User with a "user_type" of "Seller" can add a Listing
app = create_app()
response = app.test_client().get('/new_listing')

def test_add_listing():

    # Sign In User
    # Recreate Listing Form Submission
        # Validations
    # Test for Creation

    response = app.test_client().post('/add_listing')

    assert response.status_code == 'test'

# Unit Tests
    
def test_user_accessors():

    user = User(
        username='User123',
        password_hash='password',
        first_name='User123',
        last_name='User123',
        user_type='Buyer',
        email='User123@gmail.com'
    )
    assert user.first_name == 'User123'
    assert user.last_name == 'User123'
    assert user.username == 'User123'
    assert user.user_type == 'Buyer'
    assert user.email == 'User123@gmail.com'

def test_listing_accessors():
    
    listing = Listing(
        title='New Listing',
        description='New Listing',
        user_id=1,
        image='test.jpg',
        price=100
    )
    
    assert listing.title == 'New Listing'
    assert listing.description == 'New Listing'
    assert listing.user_id == 1
    assert listing.image == 'test.jpg'
    assert listing.price == 100
    
# Contact
    
def test_contact_accessors():
    
    contact = Contact(
       first_name='Test',
       last_name='Test',
       email='Test@gmail.com',
       message='Test Message'
    )
    
    assert contact.first_name == 'Test'
    assert contact.last_name == 'Test'
    assert contact.email == 'Test@gmail.com'
    assert contact.message == 'Test Message'