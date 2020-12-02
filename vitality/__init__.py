from .trainee import Trainee
from .trainer import Trainer
from .database import (
    Database,
    UsernameTakenError, WorkoutCreatorIdNotFoundError,
    password_sha256,
    InvalidCharactersException,
    UserNotFoundError
)
from .configuration import Configuration
from .workout import Workout
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
import re


def create_app():
    """Application factory for our flask web server"""
    config = Configuration()
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = 'somethingverysecret'
    app.config["MONGO_URI"] = config.get_local_uri()

    alphaPattern = re.compile(r"^[a-zA-Z0-9\s]*$")
    numberPattern = re.compile(r"^[0-9]*$")
    stringPattern = re.compile(r"^[a-zA-Z]*$")


    @app.before_request
    def before_request():
        """Actions to take before each request"""
        if 'database' not in g:
            g.database = Database(app)

        g.user = None
        if 'user_id' in session:
            g.user = g.database.get_trainee_by_id(session['user_id'])
            g.user_type = 'trainee' if g.user is not None else None

            if g.user is None:
                g.user = g.database.get_trainer_by_id(session['user_id'])
                g.user_type = 'trainer' if g.user is not None else None

    @app.route('/', methods=["GET"])
    def home():
        """The home page of Vitality"""
        app.logger.info('Rendering home')
        return render_template("home.html")

    """Account Management"""

    @app.route('/login', methods=["GET", "POST"])
    def login():
        """Login page for Vitality"""
        app.logger.info('Rendering Login')

        if request.method == 'POST':
            try:
                app.logger.debug(
                    "Poping out the the user id if found in the session.")
                session.pop('user_id', None)

                username = escape(request.form['username'])
                if not alphaPattern.search(username):
                    raise InvalidCharactersException("Invalid characters")

                password = escape(request.form['password'])
                if not alphaPattern.search(password):
                    raise InvalidCharactersException("Invalid characters")
                password = password_sha256(password)

                # Check if Trainee
                session['user_id'] = g.database.get_trainee_id_by_login(
                    username, password)
                if session['user_id']:
                    return redirect(url_for('trainee_overview'))

                # Check if Trainer
                session['user_id'] = g.database.get_trainer_id_by_login(
                    username, password)
                if session['user_id']:
                    return redirect(url_for('trainer_overview'))

                # If no user found, alert user, and reload page
                return render_template("account/login.html", login_error=True)
            except InvalidCharactersException as e:
                return render_template("account/login.html", invalid_characters=True), 400

        return render_template("account/login.html", login_error=False)

    @app.route('/signup', methods=["GET", "POST"])
    def signup():
        """Sign up page for Vitality"""
        app.logger.info('Rendering Create User')
        if request.method == 'POST':
           try:
                session.pop('user_id', None)
                username = escape(request.form['username'])
                if not alphaPattern.search(username):
                    raise InvalidCharactersException("Invalid characters")

                password = escape(request.form['password'])
                if not alphaPattern.search(password):
                    raise InvalidCharactersException("Invalid characters")

                name = escape(request.form['name'])
                if not alphaPattern.search(name):
                    raise InvalidCharactersException("Invalid characters")

                re_password = escape(request.form['repassword'])
                if not alphaPattern.search(re_password):
                    raise InvalidCharactersException("Invalid characters")

                location = escape(request.form['location'])
                if not alphaPattern.search(location):
                    raise InvalidCharactersException("Invalid characters")

                phone = escape(request.form['phone'])
                if not numberPattern.search(phone):
                    raise InvalidCharactersException("Invalid characters")

                usertype = escape(request.form['usertype'])
                if not stringPattern.search(usertype):
                    raise InvalidCharactersException("Invalid characters")

                if username and password == re_password:
                    try:
                        new_user = None
                        if usertype == 'trainee':
                            new_user = Trainee(
                                _id=None,
                                username=username,
                                password=password,
                                name=name,
                                location=location,
                                phone=phone)

                            g.database.add_trainee(new_user)

                        elif usertype == 'trainer':
                            new_user = Trainer(
                                _id=None,
                                username=username,
                                password=password,
                                name=name,
                                location=location,
                                phone=phone)

                            g.database.add_trainer(new_user)

                        else:
                            return render_template("account/signup.html", error_message=True)

                        # If username and password successful
                        return render_template("account/signup.html", creation_successful=True)

                    except UsernameTakenError as err:
                        app.logger.debug("Username {} was taken.".format(new_user))
                        return render_template("account/signup.html", username_taken=True)

                # If username and password failed, render error messsage
                return render_template("account/signup.html", error_message=True)
           except InvalidCharactersException as e:
               return render_template("account/signup.html", invalid_characters=True), 400
        return render_template("account/signup.html")

    @app.route('/profile/<username>', methods=["GET"])
    def profile(username: str):
        """Profile page for a given username"""
        if not g.user:
            app.logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        app.logger.info('Rendering Profile')
        username = escape(username)
        user = g.database.get_trainee_by_username(username)
        if user is None:
            user = g.database.get_trainer_by_username(username)
        return render_template("account/profile.html", user=user)

    @app.route('/usersettings', methods=["GET", "POST"])
    def usersettings():
        """User settings for logged in user"""
        app.logger.info('Rendering User Settings')

        if not g.user:
            return redirect(url_for('login'))

        if request.method == 'POST':
            try:
                username = escape(request.form['username'])
                if not alphaPattern.search(username):
                    raise InvalidCharactersException("Invalid characters")
                password = escape(request.form['password'])
                if not alphaPattern.search(password):
                    raise InvalidCharactersException("Invalid characters")
                name = escape(request.form['name'])
                if not stringPattern.search(name):
                    raise InvalidCharactersException("Invalid characters")
                re_password = escape(request.form['repassword'])
                if not alphaPattern.search(re_password):
                    raise InvalidCharactersException("Invalid characters")
                location = escape(request.form['location'])
                if not alphaPattern.search(location):
                    raise InvalidCharactersException("Invalid characters")
                phone = escape(request.form['phone'])
                if not numberPattern.search(phone):
                    raise InvalidCharactersException("Invalid characters")

                if g.database.get_trainee_by_id(g.user._id) is not None:

                    if username:
                        g.database.set_trainee_username(g.user._id, username)
                        if not alphaPattern.search(username):
                            raise InvalidCharactersException("Invalid characters")

                    if password and re_password and password == re_password:
                        g.database.set_trainee_password(g.user._id, password)
                        if not alphaPattern.search(password):
                            raise InvalidCharactersException("Invalid characters")

                    if location:
                        g.database.set_trainee_location(g.user._id, location)
                        if not alphaPattern.search(location):
                            raise InvalidCharactersException("Invalid characters")

                    if phone:
                        g.database.set_trainee_phone(g.user._id, phone)
                        if not numberPattern.search(phone):
                            raise InvalidCharactersException("Invalid characters")

                    if name:
                        g.database.set_trainee_name(g.user._id, name)
                        if not stringPattern.search(name):
                            raise InvalidCharactersException("Invalid characters")

                    return redirect(url_for('usersettings'))

                elif g.database.get_trainer_by_id(g.user._id) is not None:
                    if username:
                        g.database.set_trainer_username(g.user._id, username)
                        if not alphaPattern.search(username):
                            raise InvalidCharactersException("Invalid characters")

                    if password and re_password and password == re_password:
                        g.database.set_trainer_password(g.user._id, password)
                        if not alphaPattern.search(password):
                            raise InvalidCharactersException("Invalid characters")

                    if location:
                        g.database.set_trainer_location(g.user._id, location)
                        if not alphaPattern.search(location):
                            raise InvalidCharactersException("Invalid characters")

                    if phone:
                        g.database.set_trainer_phone(g.user._id, phone)
                        if not numberPattern.search(phone):
                            raise InvalidCharactersException("Invalid characters")

                    if name:
                        g.database.set_trainer_name(g.user._id, name)
                        if not stringPattern.search(name):
                            raise InvalidCharactersException("Invalid characters")

                    return redirect(url_for('usersettings'))

            except InvalidCharactersException as e:
                return render_template("account/usersettings.html", invalid_characters=True), 400

        return render_template("account/usersettings.html")

    @app.route('/delete', methods=["GET", "POST"])
    def delete():
        """Delete account page for logged in user"""
        app.logger.info('Rendering Delete account page')

        if not g.user:
            return redirect(url_for('login'))

        if request.method == 'POST':

            if g.database.get_trainee_by_id(g.user._id) is not None:
                app.logger.info('Deleting user ' + g.user.username)
                g.database.remove_trainee(session['user_id'])
                session.pop('user_id')
                return redirect(url_for('home'))

            elif g.database.get_trainer_by_id(g.user._id) is not None:
                app.logger.info('Deleting user ' + g.user.username)
                g.database.remove_trainer(session['user_id'])
                session.pop('user_id')
                return redirect(url_for('home'))

            abort(500)

        return render_template("account/delete.html")

    @app.route('/logout', methods=["GET", "POST"])
    def logout():
        """Logout route"""
        app.logger.debug('User {} has logged out.'.format(
            str(session['user_id'])))
        g.user = None
        if 'user_id' in session:
            session.pop('user_id', None)
        return redirect(url_for('home'))

    """ Trainer pages """

    @app.route('/trainer_overview', methods=["GET"])
    def trainer_overview():
        """Trainer overview page populated by current logged in trainee's g.database settings"""
        if not g.user:
            app.logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        if type(g.user) is not Trainer:
            abort(403)

        app.logger.debug('Trainer {} loaded Trainer Overview.'.format(
            str(session['user_id'])))

        trainees = []
        for trainee_id in g.user.trainees:
            trainee = g.database.get_trainee_by_id(trainee_id)
            if trainee is not None:
                trainees.append(trainee)
        peak_trainees = g.database.trainer_peak_trainees(g.user._id)
        return render_template("user/overview.html",
                               trainees=trainees,
                               workouts=g.database.get_all_workouts_by_creatorid(g.user._id),
                               events=[],
                               peak_trainees=peak_trainees)

    @app.route('/list_trainees', methods=["GET"])
    def list_trainees():
        """Trainer list trainees page which will look for all trainees that the trainer has added."""
        if not g.user:
            app.logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        if type(g.user) is not Trainer:
            app.logger.debug('Aborting becuase g.user is not a trainee.')
            abort(403)

        app.logger.debug('Trainer {} loaded Trainer List Trainees.'.format(
            str(session['user_id'])))
        trainees = []
        for trainee_id in g.user.trainees:
            trainee = g.database.get_trainee_by_id(trainee_id)
            if trainee is not None:
                trainees.append(trainee)
        return render_template("user/list_added.html",
                               users=trainees)

    @app.route('/trainer_schedule', methods=["GET"])
    def trainer_schedule():
        """Trainer schedule page which gets populated by stored event list."""
        if not g.user:
            app.logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        if type(g.user) is not Trainer:
            abort(403)

        app.logger.debug('Trainer {} loaded Trainer Schedule.'.format(
            str(session['user_id'])))
        return render_template("user/schedule.html",
                               events=[])

    """ Trainee pages """
    @app.route('/trainee_overview', methods=["GET"])
    def trainee_overview():
        """Trainee overview page which gets populated by stored event list."""
        if not g.user:
            app.logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        if type(g.user) == Trainer:
            abort(403)

        app.logger.debug('Trainee {} has loaded Trainee Overview.'.format(
            str(session['user_id'])))
        trainers = []
        for trainer_id in g.user.trainers:
            trainer = g.database.get_trainer_by_id(trainer_id)
            if trainer is not None:
                trainers.append(trainer)
        return render_template("user/overview.html",
                               trainers=trainers,
                               workouts=[])

    @app.route('/list_trainers', methods=["GET"])
    def list_trainers():
        """Trainee list trainers page which will look for all trainees that the trainer has added."""
        if not g.user:
            app.logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        if type(g.user) == Trainer:
            abort(403)

        app.logger.debug('Trainer {} loaded Trainer List Trainees.'.format(
            str(session['user_id'])))
        trainers = []
        for trainer_id in g.user.trainers:
            trainer = g.database.get_trainer_by_id(trainer_id)
            if trainer is not None:
                trainers.append(trainer)
        return render_template("user/list_added.html",
                               users=trainers)

    @app.route('/trainee_schedule', methods=["GET"])
    def trainee_schedule():
        """Trainee schedule page which gets populated by stored event list."""
        if not g.user:
            app.logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        if type(g.user) == Trainer:
            abort(403)

        app.logger.debug('Trainer {} loaded Trainer Schedule.'.format(
            str(session['user_id'])))
        return render_template("user/schedule.html",
                               events=[])

    @app.route('/trainer_search', methods=["GET", "POST"])
    def trainer_search():
        """Page for a trainee to add a trainer."""
        if not g.user:
            app.logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        if type(g.user) is not Trainee:
            abort(403)

        app.logger.debug('Trainee {} loaded add trainer page.'.format(
            str(session['user_id'])))

        if (request.method == "POST"):
            trainer_name = escape(request.form['trainer_name'])
            found_trainers = g.database.list_trainers_by_search(trainer_name)
            return render_template("trainee/trainer_search.html",
                                   trainers=found_trainers,
                                   trainer_id_list=g.user.trainers)

        return render_template("trainee/trainer_search.html")

    @app.route('/trainee_search', methods=["GET", "POST"])
    def trainee_search():
        """Page for a trainer to add a trainee."""
        if not g.user:
            app.logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        if type(g.user) is not Trainer:
            abort(403)

        app.logger.debug('Trainer {} loaded add trainer page.'.format(
            str(session['user_id'])))

        if (request.method == "POST"):
            trainee_name = escape(request.form['trainee_name'])
            found_trainees = g.database.list_trainees_by_search(trainee_name)
            return render_template("trainer/trainee_search.html",
                                   trainees=found_trainees,
                                   trainee_id_list=g.user.trainees)

        return render_template("trainer/trainee_search.html")

    @app.route('/add_trainer', methods=["POST"])
    def add_trainer():
        """This route allows trainees to add trainers to their added list"""
        if not g.user:
            app.logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        if type(g.user) is not Trainee:
            abort(403)

        try:
            trainer_id = escape(request.form['trainer_id'])
            g.database.trainee_add_trainer(g.user._id, trainer_id)
            return "", 204

        except UserNotFoundError:
            return "", 500

    @app.route('/add_trainee', methods=["POST"])
    def add_trainee():
        """This route allows trainers to add trainees to their added list"""
        if not g.user:
            app.logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        if type(g.user) is not Trainer:
            abort(403)

        try:
            trainee_id = escape(request.form['trainee_id'])
            g.database.trainer_add_trainee(g.user._id, trainee_id)
            return "", 204

        except UserNotFoundError:
            return "", 500

    """Workout pages"""
    @app.route('/new_workout', methods=["GET", "POST"])
    def new_workout():
        """Page to create a new workout"""
        if not g.user:
            return redirect(url_for('login'))

        if request.method == "POST":

            try: 
                name = escape(request.form['name'])
                about = escape(request.form['about'])
                difficulty = escape(request.form['difficulty'])

                g.database.add_workout(Workout(
                    _id=None,
                    creator_id=g.user._id,
                    name=name,
                    difficulty=difficulty,
                    about=about,
                    exp=0
                ))
                return render_template("workout/new_workout.html", workout_added = True)

            except WorkoutCreatorIdNotFoundError: 
                return render_template("workout/new_workout.html", invalid_creatorid = True)

        return render_template("workout/new_workout.html")

    @app.route('/search_workout', methods=["GET"])
    def search_workout():
        """Page to search for a workout"""
        if not g.user:
            return redirect(url_for('login'))

        return render_template("workout/search.html")

    @app.route('/workout/<workout_id>', methods=["GET"])
    def workout(workout_id: str):
        """Page that shows the workout details"""
        if not g.user:
            return redirect(url_for('login'))

        return render_template("workout/workout.html")

    @app.route('/workout_overview', methods=["GET"])
    def workout_overview():
        """Page that shows the workout details"""
        if not g.user:
            return redirect(url_for('login'))

        return render_template("workout/workout_overview.html")

    @app.route('/workout_list', methods=["GET"])
    def workout_list():
        """Page that shows the workout list"""
        if not g.user:
            return redirect(url_for('login'))

        return render_template("workout/workoutlist.html")

    @app.errorhandler(400)
    def page_bad_request(e):
        """HTTP Error 400: Bad Request Error."""
        return render_template("error/400.html"), 400

    @app.errorhandler(403)
    def page_forbidden(e):
        """HTTP Error 403: Forbidden."""
        return render_template("error/403.html"), 403

    @app.errorhandler(404)
    def page_not_found(e):
        """HTTP Error 404: Not found."""
        return render_template("error/404.html"), 404

    @app.errorhandler(410)
    def page_gone(e):
        """HTTP Error 410: Page is gone."""
        return render_template("error/410.html"), 410

    @app.errorhandler(500)
    def page_internal_error(e):
        """HTTP Error 500: Internal Server Error."""
        return render_template("error/500.html"), 500

    # Return created flask app
    return app
