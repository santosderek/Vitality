from collections import defaultdict
from logging import exception
from werkzeug.exceptions import default_exceptions
from .trainee import Trainee
from .trainer import Trainer
from .event import Event
from .database import (
    Database, EventNotFound,
    UsernameTakenError,
    WorkoutCreatorIdNotFoundError, WorkoutNotFound,
    password_sha256,
    InvalidCharactersException,
    UserNotFoundError,
    IncorrectRecipientID,
    InvitationNotFound)
from .workout import (
    Workout,
    DEFAULT_EASY_EXP,
    DEFAULT_MEDIUM_EXP,
    DEFAULT_HARD_EXP,
    DEFAULT_INSANE_EXP)
from flask import (
    abort,
    Flask,
    render_template,
    url_for,
    redirect,
    request,
    session,
    g)
from markupsafe import escape
import re
from .settings import (
    SECRET_KEY,
    MONGO_URI,
    GOOGLE_MAPS_KEY,
    GOOGLE_YOUTUBE_KEY)
import json
from datetime import datetime
from bson.errors import InvalidId
from .youtube import Youtube
import random
from googleapiclient.errors import HttpError

DEFAULT_VITALITY_PASSWORD = "DefaultVitalityTrainerPassword"


def populate_database_defaults():
    """Creates the default trainer and workouts for the application."""
    default_database = Database(MONGO_URI)

    if not default_database.get_trainer_by_username("vitality"):
        # Default Vitality User
        trainer = Trainer(
            _id=None,
            username="vitality",
            password=DEFAULT_VITALITY_PASSWORD
        )
        default_database.add_trainer(trainer)
    default_trainer = default_database.get_trainer_by_username("vitality")

    # Default Workouts
    default_workouts = [
        Workout(
            _id=None,
            creator_id=default_trainer._id,
            name="curls",
            difficulty="easy",
            about="An exercise to workout your biceps.",
            is_complete=False
        ),
        Workout(
            _id=None,
            creator_id=default_trainer._id,
            name="Russian Twists",
            difficulty="medium",
            about="An exercise to workout your abs.",
            is_complete=False
        ),
        Workout(
            _id=None,
            creator_id=default_trainer._id,
            name="burpees",
            difficulty="hard",
            about="An exercise to workout your stamina.",
            is_complete=False
        ),
        Workout(
            _id=None,
            creator_id=default_trainer._id,
            name="20lb plate pullups",
            difficulty="insane",
            about="An exercise to workout your lats, biceps, deltoids.",
            is_complete=False
        )
    ]
    for workout in default_workouts:
        try:
            default_database.get_workout_by_attributes(name=workout.name,
                                                       creator_id=workout.creator_id)
        except WorkoutNotFound:
            default_database.add_workout(workout)


def create_app():
    """Application factory for our flask web server"""
    app = Flask(__name__)
    app.secret_key = SECRET_KEY

    populate_database_defaults()

    # Input Validation
    alphaPattern = re.compile(r"^[a-zA-Z0-9\s]*$")
    numberPattern = re.compile(r"^[0-9]*$")
    stringPattern = re.compile(r"^[a-zA-Z]*$")
    lowerPattern = re.compile(r"^[a-z0-9\s]*$")

    categories = [
        'Low Carb Recipe',
        'Paleo Carb Recipe',
        'High Protein Recipe',
        'Weight Watchers Recipe',
        'Sugar Free Recipe',
        'Vegan Recipe']

    predefined_workout_topics = [
        'Abs Workout Routine',
        'Legs Workout Routine',
        'Full Body Workout'
    ]

    @app.before_request
    def before_request():
        """Actions to take before each request"""
        if 'database' not in g:
            g.database = Database(MONGO_URI)

        g.google_maps_key = GOOGLE_MAPS_KEY
        g.GOOGLE_YOUTUBE_KEY = GOOGLE_YOUTUBE_KEY

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

    @app.route('/features', methods=["GET"])
    def features():
        """The features page of Vitality"""
        app.logger.info('Rendering features page')
        return render_template("features.html")

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
                if not lowerPattern.search(username):
                    msg = "Usernames should be lowercase"
                    raise InvalidCharactersException(msg)

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
                if not lowerPattern.search(username):
                    msg = "Usernames should be lowercase"
                    raise InvalidCharactersException(msg)

                password = escape(request.form['password'])
                if not alphaPattern.search(password):
                    raise InvalidCharactersException("Invalid characters")

                name = escape(request.form['name'])
                if not alphaPattern.search(name):
                    raise InvalidCharactersException("Invalid characters")

                re_password = escape(request.form['repassword'])
                if not alphaPattern.search(re_password):
                    raise InvalidCharactersException("Invalid characters")

                phone = escape(request.form['phone'])
                if not numberPattern.search(phone):
                    raise InvalidCharactersException("Invalid characters")

                usertype = escape(request.form['usertype'])
                if not stringPattern.search(usertype):
                    raise InvalidCharactersException("Invalid characters")

                lat = float(escape(request.form['lat']))

                lng = float(escape(request.form['lng']))

                if username and password == re_password:
                    try:
                        new_user = None
                        if usertype == 'trainee':
                            new_user = Trainee(
                                _id=None,
                                username=username,
                                password=password,
                                name=name,
                                phone=phone,
                                exp=0,
                                lng=lng,
                                lat=lat)

                            g.database.add_trainee(new_user)

                        elif usertype == 'trainer':
                            new_user = Trainer(
                                _id=None,
                                username=username,
                                password=password,
                                name=name,
                                phone=phone,
                                exp=0,
                                lng=lng,
                                lat=lat)

                            g.database.add_trainer(new_user)

                        else:
                            return render_template("account/signup.html", error_message=True)
                        # If username and password successful
                        return render_template("account/signup.html", creation_successful=True)
                    except UsernameTakenError as err:
                        app.logger.debug(f"Username {username} was taken.")
                        return render_template("account/signup.html", username_taken=True)

                # If username and password failed, render error message
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

        username = escape(username)
        user = g.database.get_trainer_by_username(username) \
            or g.database.get_trainee_by_username(username)

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
                if not lowerPattern.search(username):
                    msg = "Usernames should be lowercase"
                    raise InvalidCharactersException(msg)
                password = escape(request.form['password'])
                if not alphaPattern.search(password):
                    raise InvalidCharactersException("Invalid characters")
                name = escape(request.form['name'])
                if not stringPattern.search(name):
                    raise InvalidCharactersException("Invalid characters")
                re_password = escape(request.form['repassword'])
                if not alphaPattern.search(re_password):
                    raise InvalidCharactersException("Invalid characters")
                phone = escape(request.form['phone'])
                if not numberPattern.search(phone):
                    raise InvalidCharactersException("Invalid characters")
                lat = float(escape(request.form['lat']))
                lng = float(escape(request.form['lng']))

                if g.database.get_trainee_by_id(g.user._id) is not None:
                    if username:
                        g.database.set_trainee_username(g.user._id, username)
                    if password and re_password and password == re_password:
                        g.database.set_trainee_password(g.user._id, password)
                    if phone:
                        g.database.set_trainee_phone(g.user._id, phone)
                    if name:
                        g.database.set_trainee_name(g.user._id, name)

                    if lng and lat:
                        g.database.set_coords(g.user._id, lng, lat)

                    return redirect(url_for('usersettings'))

                elif g.database.get_trainer_by_id(g.user._id) is not None:
                    if username:
                        g.database.set_trainer_username(g.user._id, username)
                    if password and re_password and password == re_password:
                        g.database.set_trainer_password(g.user._id, password)
                    if phone:
                        g.database.set_trainer_phone(g.user._id, phone)
                    if name:
                        g.database.set_trainer_name(g.user._id, name)

                    if lng and lat:
                        g.database.set_coords(g.user._id, lng, lat)

                    return redirect(url_for('usersettings'))

            except InvalidCharactersException as e:
                return render_template("account/usersettings.html", invalid_characters=True), 400

        return render_template("account/usersettings.html")

    @app.route('/remove_added_user', methods=["POST"])
    def remove_added_user():
        """Remove an added user from both the trainees and trainers list of each respective user."""

        if not g.user:
            return redirect(url_for('login'))

        try:
            confirmation = escape(request.form['confirmation'])
            user_id = escape(request.form['user_id'])

            if confirmation != 'true':
                app.logger.debug('Confirmation was not true')
                abort(500)

            if not user_id:
                app.logger.debug('User id was not given.')
                raise UserNotFoundError("User id was not given")

            if type(g.user) is Trainer:
                g.database.trainer_remove_trainee(g.user._id, user_id)
                g.database.trainee_remove_trainer(user_id, g.user._id)

            elif type(g.user) is Trainee:
                g.database.trainee_remove_trainer(g.user._id, user_id)
                g.database.trainer_remove_trainee(user_id, g.user._id)

            return '', 204

        except UserNotFoundError as error:
            message = 'Could not find a user id to delete within the added user list.'
            app.logger.debug(message)
            abort(500)

    @app.route('/delete', methods=["GET", "POST"])
    def delete():
        """Delete account page for logged in user"""
        app.logger.info('Rendering Delete account page')

        if not g.user:
            return redirect(url_for('login'))

        if request.method == 'POST':
            confirmation = escape(request.form['confirmation'])

            if str(confirmation) != 'true':
                return render_template("account/delete.html"), 500

            if g.database.get_trainee_by_id(g.user._id) is not None:
                app.logger.info('Deleting user ' + g.user.username)
                g.database.remove_trainee(session['user_id'])
                if 'user_id' in session:
                    session.pop('user_id', None)
                g.user = None
                return redirect(url_for('home'))

            elif g.database.get_trainer_by_id(g.user._id) is not None:
                app.logger.info('Deleting user ' + g.user.username)
                g.database.remove_trainer(session['user_id'])
                if 'user_id' in session:
                    session.pop('user_id', None)
                g.user = None
                return redirect(url_for('home'))

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

        # Get all trainees
        trainees = []
        for trainee_id in g.user.trainees:
            trainee = g.database.get_trainee_by_id(trainee_id)
            if trainee is not None:
                trainees.append(trainee)

        # Get all Invitations
        sent_invitations, recieved_invitations = g.database.search_all_user_invitations(
            g.user._id)

        invitations = []
        for invitation in recieved_invitations:
            invitations.append({
                'sender': g.database.get_trainee_by_id(invitation['sender']),
                'recipient': g.database.get_trainer_by_id(invitation['recipient'])
            })

        # Get all workouts
        workouts = g.database.get_all_workouts_by_creatorid(g.user._id)
        created_events, recieved_events = g.database.list_events_from_user_id(
            g.user._id)
        event_length_array = [len(created_events), len(recieved_events)]
        return render_template("user/overview.html",
                               trainees=trainees,
                               workouts=workouts,
                               invitations=invitations,
                               event_length_array=event_length_array)

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

        # Get all Invitations
        sent_invitations, recieved_invitations = g.database.search_all_user_invitations(
            g.user._id)

        invitations = []
        for invitation in recieved_invitations:
            invitations.append({
                'sender': g.database.get_trainer_by_id(invitation['sender']),
                'recipient': g.database.get_trainee_by_id(invitation['recipient'])
            })

        # Get all workouts
        workouts = g.database.get_all_workouts_by_creatorid(g.user._id)
        created_events, recieved_events = g.database.list_events_from_user_id(
            g.user._id)
        event_length_array = [len(created_events), len(recieved_events)]
        return render_template("user/overview.html",
                               trainers=trainers,
                               workouts=workouts,
                               invitations=invitations,
                               event_length_array=event_length_array)

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

    @app.route('/nearby_trainers', methods=["GET", "POST"])
    def nearby_trainers():
        """Page for trainees to see nearby trainers on a map"""
        if not g.user:
            app.logger.debug('Redirecting user because there is no g.user')
            return redirect(url_for('login'))

        if type(g.user) is not Trainee:
            abort(403)

        lat = float(g.user.lat)
        lng = float(g.user.lng)
        trainers = g.database.find_trainers_near_user(lng, lat)
        json_trainers = []

        for trainer in trainers:
            json_trainer = {
                'username': trainer.username,
                'lng': trainer.lng,
                'lat': trainer.lat
            }
            json_trainers.append(json_trainer)

        return render_template("trainee/nearby_trainers.html", json_trainers=json_trainers)

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
            g.database.create_invitation(g.user._id, trainer_id)
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
            g.database.create_invitation(g.user._id, trainee_id)
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
            name = escape(request.form['name'])
            about = escape(request.form['about'])
            difficulty = escape(request.form['difficulty'])
            total_time = escape(request.form['total_time'])
            reps = escape(request.form['reps'])
            miles = escape(request.form['miles'])
            category = escape(request.form['category'])
            try:
                existing_workout = g.database.get_workout_by_attributes(
                    creator_id=g.user._id,
                    name=name)

                app.logger.debug("Workout already exists.")
                return render_template("workout/new_workout.html", workout_name_invalid=True), 400
            except WorkoutNotFound:
                app.logger.debug("Adding new workout.")
                g.database.add_workout(Workout(
                    _id=None,
                    creator_id=g.user._id,
                    name=name,
                    difficulty=difficulty,
                    about=about,
                    is_complete=False,
                    total_time=total_time,
                    reps=reps,
                    miles=miles,
                    category=category
                ))
                return render_template("workout/new_workout.html", workout_added=True)
            except WorkoutCreatorIdNotFoundError:
                app.logger.debug("Creator Id could not be found.")
                return render_template("workout/new_workout.html", invalid_creatorid=True)
        return render_template("workout/new_workout.html")

    @app.route('/search_workout', methods=["GET", "POST"])
    def search_workout():
        """Page to search for a workout"""
        if not g.user:
            return redirect(url_for('login'))
        default_vitality_user = g.database.get_trainer_by_username("vitality")
        default_workouts = g.database.get_all_workouts_by_creatorid(
            default_vitality_user._id)

        try: 
            youtube = Youtube(g.GOOGLE_YOUTUBE_KEY)
            workout_topic = random.choice(predefined_workout_topics)
            list_of_workout_videos = youtube.search_topic(workout_topic)['items']
        except HttpError:
            list_of_workout_videos = [] 

        if request.method == "POST":
            name = escape(request.form["name"])
            workouts = g.database.get_all_workout_by_attributes(
                name={
                    '$regex': r'(.+)?{}(.+)?'.format(name)
                }
            )

            return render_template("workout/search.html",
                                   default_workouts=default_workouts,
                                   default_easy_exp=DEFAULT_EASY_EXP,
                                   default_hard_exp=DEFAULT_HARD_EXP,
                                   default_medium_exp=DEFAULT_MEDIUM_EXP,
                                   default_insane_exp=DEFAULT_INSANE_EXP,
                                   workouts=workouts,
                                   list_of_workout_videos=list_of_workout_videos)

        return render_template("workout/search.html",
                               default_workouts=default_workouts,
                               default_easy_exp=DEFAULT_EASY_EXP,
                               default_hard_exp=DEFAULT_HARD_EXP,
                               default_medium_exp=DEFAULT_MEDIUM_EXP,
                               default_insane_exp=DEFAULT_INSANE_EXP,
                               list_of_workout_videos=list_of_workout_videos)

    @app.route('/workout/<creator_id>/<workout_name>', methods=["GET", "POST"])
    def workout(creator_id: str, workout_name: str):
        """Page that shows the workout details"""
        if not g.user:
            return redirect(url_for('login'))
        creator_id = str(escape(creator_id))
        workout_name = str(escape(workout_name))

        try:
            workout_info = g.database.get_workout_by_attributes(name=workout_name,
                                                                creator_id=creator_id)
            exp_value = 0
            if workout_info.difficulty == 'easy':
                exp_value = DEFAULT_EASY_EXP
                app.logger.debug('Set exp equal to DEFAULT_EASY_EXP')

            elif workout_info.difficulty == 'medium':
                exp_value = DEFAULT_MEDIUM_EXP
                app.logger.debug('Set exp equal to DEFAULT_MEDIUM_EXP')

            elif workout_info.difficulty == 'hard':
                exp_value = DEFAULT_HARD_EXP
                app.logger.debug('Set exp equal to DEFAULT_HARD_EXP')

            elif workout_info.difficulty == 'insane':
                exp_value = DEFAULT_INSANE_EXP
                app.logger.debug('Set exp equal to DEFAULT_INSANE_EXP')

        except WorkoutNotFound:
            app.logger.debug('Workout could not be found!')
            abort(404)

        # Check creator_id and workout name, then update the workout to be completed in a POST req
        if request.method == "POST":
            completed = str(escape(request.form['completed']))
            total_time = str(escape(request.form['total_time']))
            reps = str(escape(request.form['reps']))
            miles = str(escape(request.form['miles']))
            category = str(escape(request.form['category']))
            if completed != 'true':
                abort(400)
            app.logger.debug('heyyy')
            if type(g.user) is Trainer:
                g.database.add_trainer_experience(g.user._id, exp_value)
            if type(g.user) is Trainee:
                g.database.add_trainee_experience(g.user._id, exp_value)
            g.database.set_workout_total_time(
                g.user._id, workout_name, total_time)
            g.database.set_workout_reps(g.user._id, workout_name, reps)
            g.database.set_workout_miles(g.user._id, workout_name, miles)
            g.database.set_workout_category(g.user._id, workout_name, category)
            g.database.set_workout_status(g.user._id, workout_name, True)
            workout_info = g.database.get_workout_by_attributes(name=workout_name,
                                                                creator_id=creator_id)

        return render_template("workout/workout.html", workout_info=workout_info, exp=exp_value)

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

        workouts = g.database.get_all_workouts_by_creatorid(g.user._id)

        return render_template("workout/workoutlist.html",
                               workouts=workouts)

    """Invitation System"""
    @app.route('/invitations', methods=["GET"])
    def invitations():
        """Show all sent and recieved invitations from other users."""
        if not g.user:
            app.logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        sent_invitations, recieved_invitaitons = g.database.search_all_user_invitations(
            g.user._id)

        return render_template('user/list_invitations.html',
                               all_sent=sent_invitations,
                               all_recieved=recieved_invitaitons)

    @app.route('/accept_invitation', methods=['POST'])
    def accept_invitation():
        if not g.user:
            app.logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        try:
            confirmation = escape(request.form['confirmation'])
            invitation_id = escape(request.form['invitation_id'])

            if confirmation != 'true':
                abort(500)

            g.database.accept_invitation(invitation_id, g.user._id)
            return '', 204

        except IncorrectRecipientID as error:
            app.logger.debug("There is no invitation for given recipient id.")
            abort(500)

        except InvitationNotFound as error:
            app.logger.debug("User could not find invitation!")
            abort(500)

    """Schedule"""
    @app.route('/schedule', methods=["GET"])
    def schedule():
        """Shows a users created and recieved events."""
        if not g.user:
            app.logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        app.logger.debug('User {} loaded Schedule.'.format(
            str(session['user_id'])))

        created_events, recieved_events = g.database.list_events_from_user_id(
            g.user._id)
        return render_template("user/schedule.html",
                               created_events=created_events,
                               recieved_events=recieved_events)

    @app.route('/event/<creator_id>/<event_title>', methods=["GET"])
    def event(creator_id, event_title):
        """Shows event."""
        if not g.user:
            app.logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        try:
            creator_id = escape(creator_id)
            event_title = escape(event_title)
            event = g.database.get_event_by_attributes(title=event_title,
                                                       creator_id=creator_id)
            creator = g.database.get_trainer_by_id(creator_id) or \
                g.database.get_trainee_by_id(creator_id)
            participant = g.database.get_trainer_by_id(event.participant_id) or \
                g.database.get_trainee_by_id(event.participant_id)

            return render_template("user/event.html",
                                   event=event,
                                   creator=creator,
                                   participant=participant)
        except EventNotFound:
            app.logger.debug("Event could not be found.")
            abort(404)

    @app.route('/add_event', methods=["GET", "POST"])
    def add_event():
        """Adds an event to the database."""
        if not g.user:
            app.logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        list_of_added = []
        if type(g.user) == Trainer:
            for trainee_id in g.user.trainees:
                trainee = g.database.get_trainee_by_id(trainee_id)
                list_of_added.append(trainee)

        elif type(g.user) == Trainee:
            for trainer_id in g.user.trainers:
                trainer = g.database.get_trainer_by_id(trainer_id)
                list_of_added.append(trainer)

        if request.method == 'POST':
            try:
                title = escape(request.form['title'])
                description = escape(request.form['description'])
                date = escape(request.form['date'])
                time = escape(request.form['time'])
                participant_id = escape(request.form['participant_id'])

                year, month, day = date.split('-')
                hour, minute = time.split(':')

                converted_datetime = datetime(int(year),
                                              int(month),
                                              int(day),
                                              int(hour),
                                              int(minute))
                event = Event(_id=None,
                              title=title,
                              description=description,
                              creator_id=g.user._id,
                              participant_id=participant_id,
                              date=converted_datetime)

                g.database.create_event(event)

                return render_template("user/add_event.html", list_of_added=list_of_added, success=True)

            except InvalidId:
                return render_template("user/add_event.html", list_of_added=list_of_added, invalid_participant=True)

        return render_template("user/add_event.html", list_of_added=list_of_added)

    """ Diets """
    @app.route('/diets', methods=["GET", "POST"])
    def diets():
        if not g.user:
            app.logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        return render_template('diet/diets.html', categories=categories)

    @app.route('/videos/<category>', methods=["GET"])
    def videos(category):
        if not g.user:
            app.logger.debug('Redirecting user because there is no g.user.')
            return redirect(url_for('login'))

        if not category in categories:
            abort(400)

        try: 
            youtube = Youtube(g.GOOGLE_YOUTUBE_KEY)
            youtube_videos = youtube.search_topic(category)['items']
        except Exception:
            youtube_videos = [] 
        except AttributeError:
            youtube_videos = [] 
            
        return render_template('diet/videos.html', youtube_videos=youtube_videos)

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
