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
from .trainee import Trainee
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
            app.logger.debug(
                "Poping out the the user id if found in the session.")
            session.pop('user_id', None)
            username = escape(request.form['username'])
            password = escape(request.form['password'])

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

        return render_template("account/login.html", login_error=False)

    @app.route('/signup', methods=["GET", "POST"])
    def signup():
        """Sign up page for Vitality"""
        app.logger.info('Rendering Create User')

        if request.method == 'POST':
            session.pop('user_id', None)
            username = escape(request.form['username'])
            password = escape(request.form['password'])
            name = escape(request.form['name'])
            re_password = escape(request.form['repassword'])
            location = escape(request.form['location'])
            phone = escape(request.form['phone'])
            usertype = escape(request.form['usertype'])

            if username and password == re_password:
                try:
                    new_user = None
                    if usertype == 'trainee':
                        new_user = Trainee(
                            id=None,
                            username=username,
                            password=password,
                            name=name,
                            location=location,
                            phone=phone)

                        g.database.add_trainee(new_user)

                    elif usertype == 'trainer':
                        new_user = Trainer(
                            id=None,
                            username=username,
                            password=password,
                            name=name,
                            location=location,
                            phone=phone)

                        g.database.add_trainer(new_user)

                    else:
                        redirect(url_for('signup'), 403)

                    # If username and password successful
                    return render_template("account/signup.html", creation_successful=True)

                except UsernameTakenError as err:
                    app.logger.debug("Username {} was taken.".format(new_user))
                    return render_template("account/signup.html", username_taken=True)

            # If username and password failed, render error messsage
            return render_template("account/signup.html", error_message=True)

        return render_template("account/signup.html")

    @app.route('/profile/<username>', methods=["GET"])
    def profile(username: str):
        """Profile page for a given username"""
        if not g.user:
            return redirect(url_for('login'))

        app.logger.info('Rendering Profile')
        username = escape(username)
        user = g.database.get_trainee_by_username(username)
        return render_template("account/profile.html", user=user)

    @app.route('/usersettings', methods=["GET", "POST"])
    def usersettings():
        """User settings for logged in user"""
        app.logger.info('Rendering User Settings')

        if not g.user:
            return redirect(url_for('login'))

        if request.method == 'POST':
            username = escape(request.form['username'])
            password = escape(request.form['password'])
            name = escape(request.form['name'])
            re_password = escape(request.form['repassword'])
            location = escape(request.form['location'])
            phone = escape(request.form['phone'])

            if g.database.get_trainee_by_id(g.user.id) is not None:

                if username:
                    g.database.set_trainee_username(g.user.id, username)

                if password and re_password and password == re_password:
                    g.database.set_trainee_password(g.user.id, password)

                if location:
                    g.database.set_trainee_location(g.user.id, location)

                if phone:
                    g.database.set_trainee_phone(g.user.id, phone)

                if name:
                    g.database.set_trainee_name(g.user.id, name)

                return redirect(url_for('usersettings'))

            elif g.database.get_trainer_by_id(g.user.id) is not None:
                if username:
                    g.database.set_trainer_username(g.user.id, username)

                if password and re_password and password == re_password:
                    g.database.set_trainer_password(g.user.id, password)

                if location:
                    g.database.set_trainer_location(g.user.id, location)

                if phone:
                    g.database.set_trainer_phone(g.user.id, phone)

                if name:
                    g.database.set_trainer_name(g.user.id, name)

                return redirect(url_for('usersettings'))

        return render_template("account/usersettings.html")

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

        app.logger.debug('Trainer {} is loaded Trainer Overview.'.format(
            str(session['user_id'])))
        return render_template("trainer/overview.html",
                               trainees=[],
                               workouts=[],
                               events=[])

    @app.route('/trainer_list_trainees', methods=["GET"])
    def trainer_list_trainees():
        """Trainer list trainees page which will look for all trainees that the trainer has added."""
        if not g.user:
            app.logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        if type(g.user) is not Trainer:
            app.logger.debug('Aborting becuase g.user is not a trainee.')
            abort(403)

        app.logger.debug('Trainer {} is loaded Trainer List Trainees.'.format(
            str(session['user_id'])))
        return render_template("trainer/list_trainees.html",
                               trainees=[item for item in (
                                   g.database.get_trainer_by_username("elijah"),) if item is not None])

    @app.route('/trainer_schedule', methods=["GET"])
    def trainer_schedule():
        """Trainer schedule page which gets populated by stored event list."""
        if not g.user:
            app.logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        if type(g.user) is not Trainer:
            abort(403)

        app.logger.debug('Trainer {} is loaded Trainer Schedule.'.format(
            str(session['user_id'])))
        return render_template("trainer/schedule.html",
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
        return render_template("trainee/overview.html",
                               trainers=[],
                               workouts=[]
                               )

    @app.route('/trainee_list_trainers', methods=["GET"])
    def trainee_list_trainers():
        """Trainee list trainers page which will look for all trainees that the trainer has added."""
        if not g.user:
            app.logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        if type(g.user) == Trainer:
            abort(403)

        app.logger.debug('Trainer {} is loaded Trainer List Trainees.'.format(
            str(session['user_id'])))
        return render_template("trainee/list_trainers.html",
                               trainers=[])

    @app.route('/trainee_schedule', methods=["GET"])
    def trainee_schedule():
        """Trainee schedule page which gets populated by stored event list."""
        if not g.user:
            app.logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        if type(g.user) == Trainer:
            abort(403)

        app.logger.debug('Trainer {} is loaded Trainer Schedule.'.format(
            str(session['user_id'])))
        return render_template("trainee/schedule.html",
                               events=[])

    @app.route('/trainee_add_trainer', methods=["GET", "POST"])
    def trainee_add_trainer():
        """Page for a trainer to add a trainer."""
        if not g.user:
            app.logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        if type(g.user) is not Trainee:
            abort(403)

        app.logger.debug('Trainee {} is loaded add trainer page.'.format(
            str(session['user_id'])))

        if (request.method == "POST"):
            trainer_name = escape(request.form['trainer_name'])
            found_trainers = g.database.list_trainers_by_search(trainer_name)
            return render_template("trainee/add_trainer.html", trainers=found_trainers)

        return render_template("trainee/add_trainer.html")

    """Workout pages"""
    @app.route('/new_workout', methods=["GET"])
    def new_workout():
        """Page to create a new workout"""
        if not g.user:
            return redirect(url_for('login'))

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
    def workout_overview(workout_id: str):
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
