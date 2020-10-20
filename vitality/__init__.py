from flask import (
    Flask, 
    render_template, 
    url_for, 
    request, 
    session, 
    redirect, 
    g
)
from flask_pymongo import PyMongo
from markupsafe import escape
from .user import User
from .database import Database
from .configuration import Configuration

def create_app():
    config = Configuration()
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = 'somethingverysecret'
    app.config["MONGO_URI"] = config.get_local_uri()
    logger = app.logger
    database = Database(app)
    
    @app.before_request
    def before_request():
        g.user = None
        if 'user_id' in session:
            suspected_user = database.get_user_class_by_id(session['user_id'])
            g.user = suspected_user if suspected_user and suspected_user.id == session['user_id'] else None

    @app.route('/', methods=["GET"])
    def index():
        logger.info('Rendering Index')
        return render_template("index.html")

    @app.route('/login', methods=["GET", "POST"])
    def login():
        logger.info('Rendering Login')
        
        if request.method == 'POST': 
            logger.debug("Poping out the the user id if found in the session.")
            session.pop('user_id', None)
            username = escape(request.form['username'])
            password = escape(request.form['password'])

            # This needs to be replaced once we get the database up and running
            suspected_user = database.get_user_class_by_username(username)
            found_user = suspected_user if suspected_user and suspected_user.password == password else None

            if found_user:
                logger.debug('Adding user_id to session')
                session['user_id'] = found_user.id
                return redirect(url_for('profile'))
            
            # If username and password do not match
            return redirect(url_for('login'))

        return render_template("login.html")

    @app.route('/createuser', methods=["GET", "POST"])
    def createuser():
        logger.info('Rendering Create User')

        if request.method == 'POST':
            session.pop('user_id', None)
            username = escape(request.form['username'])
            password = escape(request.form['password'])
            firstname = escape(request.form['firstname'])
            lastname = escape(request.form['lastname'])
            re_password = escape(request.form['repassword'])
            location = escape(request.form['location'])
            phone = escape(request.form['phone'])

            if username and password == re_password:
                new_user = User(
                    id = None, 
                    username = username, 
                    password = password, 
                    firstname = firstname, 
                    lastname = lastname, 
                    location = location, 
                    phone = phone)
                database.add_user(new_user)
                return redirect(url_for('login'))
                #TODO: need to show user it was successful. 

        return render_template("createuser.html")

    @app.route('/profile', methods=["GET"])
    def profile():
        logger.info('Rendering Profile')

        if not g.user:
            return redirect(url_for('login'))
        return render_template("profile.html")
    
    @app.route('/usersettings', methods=["GET","POST"])
    def usersettings():
        logger.info('Rendering User Settings')

        if not g.user:
            return redirect(url_for('login'))

        if request.method == 'POST':
            username = escape(request.form['username'])
            password = escape(request.form['password'])
            firstname = escape(request.form['firstname'])
            lastname = escape(request.form['lastname'])
            re_password = escape(request.form['repassword'])
            location = escape(request.form['location'])
            phone = escape(request.form['phone'])

            if username and password == re_password:
                database.set_username(g.user.id, username)
                database.set_password(g.user.id, password)
                database.set_location(g.user.id, location)
                database.set_phone(g.user.id, phone)
                database.set_firstname(g.user.id, firstname)
                database.set_lastname(g.user.id, lastname)

                g.user = database.get_user_class_by_id(g.user.id)
                return redirect(url_for('usersettings'))

            
        return render_template("usersettings.html")

    @app.errorhandler(403)
    def page_not_found(e):
        logger.info('Rendering 403')
        return "403", 403
    
    @app.errorhandler(404)
    def page_not_found(e):
        logger.info('Rendering 404')
        return "404", 404
    
    @app.errorhandler(410)
    def page_not_found(e):
        logger.info('Rendering 410')
        return "410", 410
    
    @app.errorhandler(500)
    def page_not_found(e):
        logger.info('Rendering 500')
        return "500", 500

    # Return for Application Factory
    return app

