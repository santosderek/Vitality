from flask import (
    abort,
    Flask,
    render_template,
    url_for,
    redirect,
    request,
    session,
    g
)
from flask_pymongo import PyMongo
from markupsafe import escape
from .user import User
from .trainer import Trainer
from .database import Database, UsernameTakenError
from .configuration import Configuration
from .workout import Workout


def create_app():
    """Application factory for our flask web server"""
    config = Configuration()
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = 'somethingverysecret'
    app.config["MONGO_URI"] = config.get_local_uri()
    logger = app.logger
    database = Database(app)

    @app.before_request
    def before_request():
        """Actions to take before each request"""
        g.user = None
        if 'user_id' in session:
            suspected_user = database.get_user_class_by_id(session['user_id'])
            if suspected_user and suspected_user.id == session['user_id']:
                g.user = suspected_user

            else:
                g.user = None

    @app.route('/', methods=["GET"])
    def home():
        """The home page of Vitality"""
        logger.info('Rendering home')
        return render_template("home.html")

    """Account Management"""

    @app.route('/login', methods=["GET", "POST"])
    def login():
        """Login page for Vitality"""
        logger.info('Rendering Login')

        if request.method == 'POST':
            logger.debug("Poping out the the user id if found in the session.")
            session.pop('user_id', None)
            username = escape(request.form['username'])
            password = escape(request.form['password'])

            # This needs to be replaced once we get the database up and running
            suspected_user = database.get_user_class_by_username(username)
            found_user = suspected_user if suspected_user and suspected_user.password == password else None

            if found_user and type(found_user) == Trainer:
                logger.debug('Adding user_id to session')
                session['user_id'] = found_user.id
                return redirect(url_for('trainer_overview'))

            elif found_user and type(found_user) == User:
                logger.debug('Adding user_id to session')
                session['user_id'] = found_user.id
                return redirect(url_for('trainee_overview'))

            # If no user found, alert user, and reload page
            return render_template("account/login.html", login_error=True)

        return render_template("account/login.html", login_error=False)

    @app.route('/signup', methods=["GET", "POST"])
    def signup():
        """Sign up page for Vitality"""
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
                try:
                    database.add_user(new_user)
                    # If username and password successful
                    return render_template("account/signup.html", creation_successful=True)
                except UsernameTakenError as err:
                    logger.debug("Username {} was taken.".format(new_user))
                    return render_template("account/signup.html", username_taken=True)

            # If username and password failed, render error messsage
            return render_template("account/signup.html", error_message=True)

        return render_template("account/signup.html")

    @app.route('/profile/<username>', methods=["GET"])
    def profile(username):
        """Profile page for a given username"""
        if not g.user:
            return redirect(url_for('login'))

        logger.info('Rendering Profile')
        username = escape(username)
        user = database.get_user_class_by_username(username)
        return render_template("account/profile.html", user=user)

    @app.route('/usersettings', methods=["GET", "POST"])
    def usersettings():
        """User settings for logged in user"""
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
        """Logout route"""
        logger.debug('User {} has logged out.'.format(str(session['user_id'])))
        g.user = None
        if 'user_id' in session:
            session.pop('user_id', None)
        return redirect(url_for('home'))

    """ Trainer pages """

    @app.route('/trainer_overview', methods=["GET"])
    def trainer_overview():
        """Trainer overview page populated by current logged in user's database settings"""
        if not g.user:
            logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        if type(g.user) != Trainer:
            abort(403)

        logger.debug('Trainer {} is loaded Trainer Overview.'.format(
            str(session['user_id'])))
        return render_template("trainer/overview.html",
                               trainees=[
                                   database.get_user_class_by_username(
                                       "derek"),
                                   database.get_user_class_by_username(
                                       "bryson"),
                                   database.get_user_class_by_username("elijah")],
                               workouts=[
                                   Workout(id=None, creator_id="1", name="Workout 1",
                                           difficulty="easy", exp_rewards=0),
                                   Workout(id=None, creator_id="1", name="Workout 1",
                                           difficulty="easy", exp_rewards=0),
                                   Workout(id=None, creator_id="1", name="Workout 1",
                                           difficulty="easy", exp_rewards=0)
                               ],
                               events=[])

    @app.route('/trainer_list_trainees', methods=["GET"])
    def trainer_list_trainees():
        """Trainer list trainees page which will look for all trainees that the trainer has added."""
        if not g.user:
            logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))
        
        if type(g.user) != Trainer:
            abort(403)

        logger.debug('Trainer {} is loaded Trainer List Trainees.'.format(
            str(session['user_id'])))
        return render_template("trainer/list_trainees.html",
                               trainees=[
                                   database.get_user_class_by_username(
                                       "derek"),
                                   database.get_user_class_by_username(
                                       "bryson"),
                                   database.get_user_class_by_username("elijah")])

    @app.route('/trainer_schedule', methods=["GET"])
    def trainer_schedule():
        """Trainer schedule page which gets populated by stored event list."""
        if not g.user:
            logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))
        
        if type(g.user) != Trainer:
            abort(403)

        logger.debug('Trainer {} is loaded Trainer Schedule.'.format(
            str(session['user_id'])))
        return render_template("trainer/schedule.html",
                               events=[])

    """ Trainee pages """
    @app.route('/trainee_overview', methods=["GET"])
    def trainee_overview():
        """Trainee overview page which gets populated by stored event list."""
        if not g.user:
            logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))
        
        if type(g.user) == Trainer:
            abort(403)

        logger.debug('Trainee {} has loaded Trainee Overview.'.format(
            str(session['user_id'])))
        return render_template("trainee/overview.html",
                               trainers=[
                                   database.get_user_class_by_username(
                                       "derek"),
                                   database.get_user_class_by_username(
                                       "bryson"),
                                   database.get_user_class_by_username("elijah")],
                               workouts=[
                                   Workout(id=None, creator_id="1", name="Workout 1",
                                           difficulty="easy", exp_rewards=0),
                                   Workout(id=None, creator_id="1", name="Workout 1",
                                           difficulty="easy", exp_rewards=0),
                                   Workout(id=None, creator_id="1", name="Workout 1", difficulty="easy", exp_rewards=0)]
                               )

    @app.route('/trainee_list_trainers', methods=["GET"])
    def trainee_list_trainers():
        """Trainee list trainers page which will look for all trainees that the trainer has added."""
        if not g.user:
            logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))
        
        if type(g.user) == Trainer:
            abort(403)

        logger.debug('Trainer {} is loaded Trainer List Trainees.'.format(
            str(session['user_id'])))
        return render_template("trainee/list_trainers.html",
                               trainers=[
                                   database.get_user_class_by_username(
                                       "derek"),
                                   database.get_user_class_by_username(
                                       "bryson"),
                                   database.get_user_class_by_username("elijah")])

    @app.route('/trainee_schedule', methods=["GET"])
    def trainee_schedule():
        """Trainee schedule page which gets populated by stored event list."""
        if not g.user:
            logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))
        
        if type(g.user) == Trainer:
            abort(403)

        logger.debug('Trainer {} is loaded Trainer Schedule.'.format(
            str(session['user_id'])))
        return render_template("trainee/schedule.html",
                               events=[])

    @app.errorhandler(403)
    def page_not_found(e):
        """HTTP Error 403: Forbidden."""
        return render_template("error/403.html"), 403

    @app.errorhandler(404)
    def page_not_found(e):
        """HTTP Error 404: Not found."""
        return render_template("error/404.html"), 404

    @app.errorhandler(410)
    def page_not_found(e):
        """HTTP Error 410: Page is gone."""
        return render_template("error/410.html"), 410

    @app.errorhandler(500)
    def page_not_found(e):
        """HTTP Error 500: Internal Server Error."""
        return render_template("error/500.html"), 500

    # Return created flask app
    return app
