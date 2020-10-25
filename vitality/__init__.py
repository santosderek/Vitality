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
from .workout import Workout

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
            if suspected_user and suspected_user.id == session['user_id']:
                g.user = suspected_user

            else:
                g.user = None

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

            # If no user found, alert user, and reload page
            return render_template("account/login.html", login_error=True)

        return render_template("account/login.html", login_error=False)

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
                    id=None,
                    username=username,
                    password=password,
                    firstname=firstname,
                    lastname=lastname,
                    location=location,
                    phone=phone)
                database.add_user(new_user)
                # If username and password successful
                return render_template("account/createuser.html", creation_successful=True, error_message=False)

            # If username and password failed, render error messsage
            return render_template("account/createuser.html", creation_successful=True, error_message=True)

        return render_template("account/createuser.html", creation_successful=False, error_message=False)

    @app.route('/profile/<username>', methods=["GET"])
    def profile(username):
        logger.info('Rendering Profile')
        username = escape(username)
        user = database.get_user_class_by_username(username)
        return render_template("account/profile.html", user=user)


    @app.route('/usersettings', methods=["GET", "POST"])
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

            if session['user_id'] == database.get_user_class_by_username(g.user.username).id:

                if username:
                    database.set_username(g.user.id, username)

                if password and re_password and password == re_password:
                    database.set_password(g.user.id, password)

                if location:
                    database.set_location(g.user.id, location)

                if phone:
                    database.set_phone(g.user.id, phone)

                if firstname:
                    database.set_firstname(g.user.id, firstname)

                if lastname:
                    database.set_lastname(g.user.id, lastname)

                return redirect(url_for('usersettings'))

        return render_template("account/usersettings.html")

    @app.route('/logout', methods=["GET", "POST"])
    def logout():
        logger.debug('User {} has logged out.'.format(str(session['user_id'])))
        g.user = None
        if 'user_id' in session:
            session.pop('user_id', None)
        return redirect(url_for('index'))


    """ Trainer pages """
    
    @app.route('/trainer_overview', methods=["GET"])
    def trainer_overview():
        if not g.user:
            logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        logger.debug('Trainer {} is loaded Trainer Overview.'.format(str(session['user_id'])))
        return render_template("trainer/overview.html", 
            trainees=[
                database.get_user_class_by_username("derek"),
                database.get_user_class_by_username("bryson"),
                database.get_user_class_by_username("elijah")], 
            workouts=[
                Workout(id=None, creator_id="1", name="Workout 1", difficulty="easy", exp_rewards=0),
                Workout(id=None, creator_id="1", name="Workout 1", difficulty="easy", exp_rewards=0),
                Workout(id=None, creator_id="1", name="Workout 1", difficulty="easy", exp_rewards=0)
            ],
            events=[])

    @app.route('/trainer_list_trainees', methods=["GET"])
    def trainer_list_trainees():
        if not g.user:
            logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        logger.debug('Trainer {} is loaded Trainer List Trainees.'.format(str(session['user_id'])))
        return render_template("trainer/list_trainees.html", 
            trainees=[
                database.get_user_class_by_username("derek"),
                database.get_user_class_by_username("bryson"),
                database.get_user_class_by_username("elijah")])
    
    @app.route('/trainer_schedule', methods=["GET"])
    def trainer_schedule():
        if not g.user:
            logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        logger.debug('Trainer {} is loaded Trainer Schedule.'.format(str(session['user_id'])))
        return render_template("trainer/schedule.html", 
            events=[])

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
