import os
from flask import Flask, redirect, request, url_for, send_from_directory
from flask import render_template
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, user_logged_in
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from forms import NewListingForm, NewUserForm, LoginForm, ContactForm, NewPasswordForm
from models import User, Listing, Contact, db
from datetime import datetime, timedelta
from sqlalchemy import exc

import pymysql
pymysql.install_as_MySQLdb()

# Listings vs. Users -> One to Many Relationship
    # One User / Many Listings
        # Listings are going to store the foreign key (user_id)

    # u = User.new(id: 1, firstNAme: "Louis", lastName: "Medina", userType: "Seller")
    # l = Listing.new(id: 1, title: "My Car", description: "New Car For Sale", userId: 1)

# Full Stack Application
    # Right Now - Just Flask
    # In A Full STack Application - React Front End, Flask Back End

#  File Uploads

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# To Do: Create UpdatePassword Form
    # A visual sketch should be helpful for us

login_manager = LoginManager()

def create_app():
    app = Flask(
        __name__,
        static_url_path="",
        static_folder="static"
    )
    app.config.from_object(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost:3306/CS4417'

    db.init_app(app)

    login_manager.login_view = "login"
    login_manager.init_app(app)

    app.secret_key = "*( change me)"

    # seeder = FlaskSeeder()
    # seeder.init_app(app, db)

    @login_manager.user_loader
    def load_user(user_id):
        print(f'load_user() called: {user_id}')
        user = db.session.query(User).filter_by(id=user_id).one()
        return user

    def get_user(username, password):

        # To Do: We need to check more than whether or not a "username" exists in the database. We need to 
        # check the passed "password" to make sure that it matches the password for the specified user.

        # Sessions: If encryption is required, we can incorporate the Flask-Login Extension

        user = db.session.query(User).filter_by(username=username).one()

        if user:
            # Pull the "password_hash" from the DB for the found User
            password_hash = user.password_hash
            # Use "check_password_hash" to compare the plain-text password submitted with the 
            # Login Form (password) with the hashed password stored in the DB (password_hash)
            is_valid = check_password_hash(password_hash, password)
            #  If "is_valid" is True, we return the User
            if is_valid:
                return user
        
        # cnx.close()

    def handle_update_password(username, new_password, old_password):
        
        # With "oldPassword", we've got to verify that this matches the User's
        # current password before issuing a change to the DB.

        user = db.session.query(User).filter_by(username=username).one()
        password_hash = user.password_hash
        is_valid = check_password_hash(password_hash, old_password)

        if is_valid:

            hashed_new_password = generate_password_hash(new_password)
            user.password_hash = hashed_new_password

            db.session.add(user)
            db.session.commit()

            return user

    def handle_add_user(username, password, first_name, last_name, user_type, email):

        # Converts Plain Text Form Value for "password" to an Encrypted Hash + Salt
        encrypted_password = generate_password_hash(password)

        new_user = User(
            username=username,
            password_hash=encrypted_password,
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
            email=email
        )

        db.session.add(new_user)
        db.session.commit()

        print("User Created Successfully")

    # Routes -> Endpoints That Can Receive Any Kind of HTTP Verb:
        # 1) GET -> Retrieving Information
        # 2) POST -> Sending Information
        # 3) PATCH / PUT -> Updating Information
        # 4) DELETE -> Destroying Information

    # Sellers
            
    # Method to Show Seller's Listings

    def get_my_listings(seller_id):
        listings = db.session.query(Listing).filter_by(user_id=seller_id).all()
        return listings
        
    #  Method to Retrieve Inidividual Listing
        
    def get_listing(listing_id):
        listing = db.session.query(Listing).filter_by(id=listing_id).one()
        return listing

        
    def handle_add_listing(title, description, user_id, image, price):

        new_listing = Listing(
            title=title,
            description=description,
            user_id=user_id,
            image=image,
            price=price
        )

        db.session.add(new_listing)
        db.session.commit()
        return new_listing
        
    # Buyers

    def get_all_listings():
        listings = db.session.query(Listing).all()
        return listings

    def handle_add_contact(first_name, last_name, email, message):

        new_contact = Contact(
            first_name=first_name,
            last_name=last_name,
            email=email,
            message=message
        )
            
        db.session.add(new_contact)    
        db.session.commit()

        print("Contact Created Successfully")

    def check_logout():
        if current_user.is_authenticated:
            last_active = current_user.last_active

            if datetime.utcnow() - last_active > timedelta(minutes=1):
                return redirect (url_for('logout'))

# Routes

    @app.route("/")
    @login_required
    def index():
        print('Showing home page')
        return render_template("home.html") 

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        
        form = LoginForm()

        # What we should do when a form is being submitted
        if form.validate_on_submit():
            username=form.username.data
            password=form.password.data
            print(f"trying to log in as {username}")


            retrievedUser = get_user(username, password)
            if retrievedUser:
                print(f"logged in as {username}")
                userType = retrievedUser.user_type
                login_user(retrievedUser)
                return redirect(url_for('index', userType=userType))
            else:
                error = 'Incorrect Username or Password'  
                return render_template('login.html', error=error, form=form)


        # What we should do if this page is redirected to from "/contact"
        if request.referrer and '/contact' in request.referrer:
            confirmation = 'Thanks for getting in touch with us!' 

            return render_template('login.html', form=form, confirmation=confirmation)

        print('Showing login page')  
        return render_template("login.html", form=form)

    @app.route('/register', methods=['GET', 'POST'])
    def register():

        form = NewUserForm()

        logout_user() # -> Clear Out User Session That Was Potentially in Place Before

        if form.validate_on_submit():
            password=form.password.data
            username=form.username.data
            first_name=form.first_name.data
            last_name=form.last_name.data
            user_type=form.user_type.data
            email=form.email.data

            print(f"trying to register in as {username}")

            try:
            
                handle_add_user(username, password, first_name, last_name, user_type, email)

                retrievedUser = get_user(username, password)

                login_user(retrievedUser)
                
                return redirect(url_for('index'))
            
            except exc.SQLAlchemyError as e:

                error_message = "Username Taken"

                return render_template("register.html", form=form, error_message=error_message)
            
        print('Showing registration page')
        return render_template("register.html", form=form)
        
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        print('Logot user called')
        return redirect('/login')

    @app.route('/password', methods=['GET', 'POST'])
    @login_required
    def password():
        
        form = NewPasswordForm()

        username = current_user.username
        
        if form.validate_on_submit():
            newPassword=form.new_password.data
            oldPassword=form.old_password.data

            updated_user = handle_update_password(username, newPassword, oldPassword)

            if updated_user:
                confirmation_message = "Password Updated!"
                return render_template("home.html", confirmation_message=confirmation_message)
            else:
                error_message = "Old Password Incorrect"
                return render_template("password.html", error_message=error_message,  form=form)

        
        return render_template("password.html", form=form)    

    @app.route("/feedback") 
    @login_required
    def feedback():
        return render_template("feedback.html")

    # Contact Page
        # 1) Store Information
        # 2) Configure Mailer (*) (https://pythonhosted.org/Flask-Mail/)

    @app.route('/contact', methods=['GET', 'POST']) 
    def contact():

        form = ContactForm()

        if form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            message = form.message.data

            handle_add_contact(first_name, last_name, email, message)

            return redirect(url_for('login'))

        return render_template('contact.html', form=form)

    @app.route('/profile') 
    @login_required
    def profile():
        return render_template('profile.html')

    # Listings Routes

    @app.route('/<user_id>/my_listings')
    @login_required
    def my_listings(user_id):
        listings = get_my_listings((user_id, )) 

        # In every route, we always have a "request" object implicitly available to us
        # We can build out conditional behaviors based upon properties of each "request" object
            # Example => if request.method == "POST"
        if request.referrer and '/new_listing' in request.referrer:
            confirmation = 'New Listing Added!'

            return render_template('my_listings.html', listings=listings, confirmation=confirmation)

        return render_template('my_listings.html', listings=listings)

    @app.route('/uploads/<filename>')
    def get_image(filename):
        # Retrieve the image file from the /uploads directory
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    @app.route("/listings/<listing_id>")
    @login_required
    def show_listing(listing_id):
        # Retrieve listing
        listing = get_listing((listing_id, ))
        
        return render_template('listing.html', listing=listing)

    @app.route("/new_listing", methods=['GET', 'POST'])
    @login_required
    def add_new_listing():

        form = NewListingForm()
        
        user_id = current_user.id

        print(user_id)

        if form.validate_on_submit():
            title=form.title.data
            description=form.description.data
            price=form.price.data
            image_file = form.image.data

            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            handle_add_listing(title, description, user_id, image_file.filename, price)

            return redirect(f"{user_id}/my_listings")

        return render_template('new_listing.html', form=form)

    @app.route("/listings")
    @login_required
    def listings():
        listings = get_all_listings()
        print(listings)

        return render_template('all_listings.html', listings=listings)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run()