from datetime import datetime
from bson.objectid import ObjectId
from flask.globals import request
import pytest
from flask import g, session, url_for
from os import environ
from vitality import create_app
from vitality import database
from vitality.database import Database, WorkoutCreatorIdNotFoundError, password_sha256, InvalidCharactersException
from vitality.trainee import Trainee
from vitality.trainer import Trainer
from vitality.workout import Workout
from vitality.event import Event
from vitality.settings import MONGO_URI, SECRET_KEY
from datetime import datetime
from dotenv import load_dotenv 
from time import sleep

test_trainee = Trainee(
    _id=None,
    username="testtrainee",
    password="password",
    name="first last",
    phone=1234567890
)

test_trainer = Trainer(
    _id=None,
    username="testtrainer",
    password="password",
    name="first last",
    phone=1234567890
)


def login_as_testTrainee(client):
    """Login as testTrainee"""
    returned_value = client.post('/login', data=dict(
        username="testtrainee",
        password="password"
    ), follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'Could not log you in!' not in returned_value.data
    assert b'Add Trainer' in returned_value.data
    assert b'Workouts' in returned_value.data
    assert b'Schedule' in returned_value.data


def login_as_testTrainer(client):
    """Login as testTrainer"""
    returned_value = client.post('/login', data=dict(
        username="testtrainer",
        password="password"
    ), follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'Could not log you in!' not in returned_value.data
    assert b'Add Trainee' in returned_value.data
    assert b'Workouts' in returned_value.data
    assert b'Schedule' in returned_value.data


@pytest.fixture
def client():
    environ['SECRET_KEY'] = 'aTestSecret'
    load_dotenv('.env')
    app = create_app()
    app.config['TESTING'] = True
    app.secret_key = environ.get('SECRET_KEY')
    database = Database(MONGO_URI)

    def setup():
        """ Code run after client has been used """
        teardown()
        database.add_trainer(test_trainer)
        database.add_trainee(test_trainee)

    def teardown():
        """ Code run after client has been used """
        while database.get_trainee_by_username("testtrainee"):
            database.remove_trainee(
                database.get_trainee_by_username("testtrainee")._id)

        while database.get_trainer_by_username("testtrainer"):
            database.remove_trainer(
                database.get_trainer_by_username("testtrainer")._id)

    with app.test_client() as client:
        with app.app_context():
            setup()
            yield client
            teardown()


def test_failed_login_username(client):
    # Testing the failed login page
    returned_value = client.post('/login', data=dict(
        username="testtrainee#%#^",
        password="password"
    ), follow_redirects=True)
    assert returned_value.status_code == 400
    assert b'Invalid characters found' in returned_value.data
    assert g.user is None


def test_failed_login_username_uppercase(client):
    # Testing the failed login page
    returned_value = client.post('/login', data=dict(
        username="testTrainee",
        password="password"
    ), follow_redirects=True)
    assert returned_value.status_code == 400
    assert b'Invalid characters found' in returned_value.data
    assert g.user is None


def test_failed_login_password(client):
    # Testing the failed login page
    returned_value = client.post('/login', data=dict(
        username="testtrainee",
        password="password#^#$#"
    ), follow_redirects=True)
    assert returned_value.status_code == 400
    assert b'Invalid characters found' in returned_value.data
    assert g.user is None


def test_failed_signup_username(client):
    # Testing the failed signup page
    returned_value = client.post('/signup', data=dict(
        username="testtrainee^#$^%^",
        password="password",
        name="test",
        repassword="password",
        phone="12345678",
        usertype="trainee"
    ), follow_redirects=True)
    assert returned_value.status_code == 400
    assert b'Invalid characters found' in returned_value.data
    assert g.user is None


def test_failed_signup_username_uppercase(client):
    # Testing the failed signup page
    returned_value = client.post('/signup', data=dict(
        username="testTrainee",
        password="password",
        name="test",
        repassword="password",
        phone="12345678",
        usertype="trainee"
    ), follow_redirects=True)
    assert returned_value.status_code == 400
    assert b'Invalid characters found' in returned_value.data
    assert g.user is None


def test_failed_signup_password(client):
    # Testing the failed signup page
    returned_value = client.post('/signup', data=dict(
        username="testtrainee",
        password="password^#$^%^",
        name="test",
        repassword="password",
        phone="12345678",
        usertype="trainee"
    ), follow_redirects=True)
    assert returned_value.status_code == 400
    assert b'Invalid characters found' in returned_value.data
    assert g.user is None


def test_failed_signup_name(client):
    # Testing the failed signup page
    returned_value = client.post('/signup', data=dict(
        username="testtrainee",
        password="password",
        name="1245667*#",
        repassword="password",
        phone="12345678",
        usertype="trainee"
    ), follow_redirects=True)
    assert returned_value.status_code == 400
    assert b'Invalid characters found' in returned_value.data
    assert g.user is None


def test_failed_signup_repassword(client):
    # Testing the failed signup page
    returned_value = client.post('/signup', data=dict(
        username="testtrainee",
        password="password",
        name="test",
        repassword="password^#$^%",
        phone="12345678",
        usertype="trainee"
    ), follow_redirects=True)
    assert returned_value.status_code == 400
    assert b'Invalid characters found' in returned_value.data
    assert g.user is None


def test_failed_signup_phone(client):
    # Testing the failed signup page
    returned_value = client.post('/signup', data=dict(
        username="testtrainee",
        password="password",
        name="test",
        repassword="password",
        phone="phone",
        usertype="trainee"
    ), follow_redirects=True)
    assert returned_value.status_code == 400
    assert b'Invalid characters found' in returned_value.data
    assert g.user is None


def test_failed_signup_usertype(client):
    # Testing the failed signup page
    returned_value = client.post('/signup', data=dict(
        username="testtrainee",
        password="password",
        name="test",
        repassword="password",
        phone="12345678",
        usertype="117"
    ), follow_redirects=True)
    assert returned_value.status_code == 400
    assert b'Invalid characters found' in returned_value.data
    assert g.user is None


def test_failed_usersettings_username(client):
    # Testing the failed user settings page
    # Get without a user

    returned_value = client.get('/usersettings', follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'login' in returned_value.data

    # Login as trainee
    login_as_testTrainee(client)

    # Check profile page.
    returned_value = client.post('/usersettings', data=dict(
        username="testtrainee^#$^%^",
        password="password",
        name="test",
        repassword="password",
        phone="12345678",
    ), follow_redirects=True)
    assert returned_value.status_code == 400
    assert b'Invalid characters found' in returned_value.data


def test_failed_usersettings_username_uppercase(client):
    # Testing the failed user settings page
    # Get without a user

    returned_value = client.get('/usersettings', follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'login' in returned_value.data

    # Login as trainee
    login_as_testTrainee(client)

    # Check profile page.
    returned_value = client.post('/usersettings', data=dict(
        username="testTrainee",
        password="password",
        name="test",
        repassword="password",
        phone="12345678",
    ), follow_redirects=True)
    assert returned_value.status_code == 400
    assert b'Invalid characters found' in returned_value.data


def test_failed_usersettings_password(client):
    # Testing the failed user settings page
    # Get without a user

    returned_value = client.get('/usersettings', follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'login' in returned_value.data

    # Login as trainee
    login_as_testTrainee(client)

    # Check profile page.
    returned_value = client.post('/usersettings', data=dict(
        username="testtrainee",
        password="password^#$^%^",
        name="test",
        repassword="password",
        phone="12345678",
    ), follow_redirects=True)
    assert returned_value.status_code == 400
    assert b'Invalid characters found' in returned_value.data


def test_failed_usersettings_repassword(client):
    # Testing the failed user settings page
    # Get without a user

    returned_value = client.get('/usersettings', follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'login' in returned_value.data

    # Login as trainee
    login_as_testTrainee(client)

    # Check profile page.
    returned_value = client.post('/usersettings', data=dict(
        username="testtrainee",
        password="password",
        name="test",
        repassword="password^#$^%^",
        phone="12345678",
    ), follow_redirects=True)
    assert returned_value.status_code == 400
    assert b'Invalid characters found' in returned_value.data


def test_failed_usersettings_name(client):
    # Testing the failed user settings page
    # Get without a user

    returned_value = client.get('/usersettings', follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'login' in returned_value.data

    # Login as trainee
    login_as_testTrainee(client)

    # Check profile page.
    returned_value = client.post('/usersettings', data=dict(
        username="testtrainee",
        password="password",
        name="117",
        repassword="password",
        phone="12345678",
    ), follow_redirects=True)
    assert returned_value.status_code == 400
    assert b'Invalid characters found' in returned_value.data


"""def test_failed_usersettings_location(client):
    # Testing the failed user settings page
    # Get without a user

    returned_value = client.get('/usersettings', follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'login' in returned_value.data

    # Login as trainee
    login_as_testTrainee(client)

    # Check profile page.
    returned_value = client.post('/usersettings', data=dict(
        username="testtrainee",
        password="password",
        name="test",
        repassword="password",
        phone="12345678",
    ), follow_redirects=True)
    assert returned_value.status_code == 400
    assert b'Invalid characters found' in returned_value.data"""


def test_failed_usersettings_phone(client):
    # Testing the failed user settings page
    # Get without a user

    returned_value = client.get('/usersettings', follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'login' in returned_value.data

    # Login as trainee
    login_as_testTrainee(client)

    # Check profile page.
    returned_value = client.post('/usersettings', data=dict(
        username="testtrainee",
        password="password",
        name="test",
        repassword="password",
        phone="phone",
    ), follow_redirects=True)
    assert returned_value.status_code == 400
    assert b'Invalid characters found' in returned_value.data


def test_home(client):
    """Testing the home page"""
    returned_value = client.get('/', follow_redirects=True)
    assert returned_value.status_code == 200


def test_features(client):
    """Testing the home page"""
    returned_value = client.get('/features', follow_redirects=True)
    assert returned_value.status_code == 200


def test_login(client):
    """Testing the login page"""
    # Get without a user
    returned_value = client.get('/login', follow_redirects=True)
    assert returned_value.status_code == 200

    # POST with a user
    login_as_testTrainee(client)

    # POST with a fake user
    returned_value = client.post('/login', data=dict(
        username="fake",
        password="password"
    ), follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'Could not log you in!' in returned_value.data
    assert b'Add Trainer' not in returned_value.data
    assert b'Username' in returned_value.data
    assert b'Password' in returned_value.data
    assert b'Login</button>' in returned_value.data
    assert b'Remember me</label>' in returned_value.data


def test_signup(client):
    """Testing the sign up page"""

    def clean_up(trainer, trainee):
        g.database.mongo.trainer.delete_many({
            '_id': ObjectId(trainer._id)
        })
        g.database.mongo.trainee.delete_many({
            '_id': ObjectId(trainee._id)
        })

    # Get without a user
    returned_value = client.get('/signup', follow_redirects=True)
    assert returned_value.status_code == 200

    # POST with a wrong password combination
    returned_value = client.post('/signup', data=dict(
        username="testtrainee",
        password="password",
        repassword="repassword",
        name="first last",
        phone=1234567890,
        usertype="trainee",
        lng=0,
        lat=0
    ), follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'Account was created!' not in returned_value.data
    assert b'Could not create account' in returned_value.data
    assert b'Username was taken' not in returned_value.data
    assert b'<form action="/signup" method="POST">' in returned_value.data

    # POST with a wrong usertype
    returned_value = client.post('/signup', data=dict(
        username="testtrainee",
        password="password",
        repassword="password",
        name="first last",
        phone=1234567890,
        usertype="notausertype",
        lng=0,
        lat=0
    ), follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'Account was created!' not in returned_value.data
    assert b'Could not create account' in returned_value.data
    assert b'Username was taken' not in returned_value.data
    assert b'<form action="/signup" method="POST">' in returned_value.data

    # POST with a username that was taken
    returned_value = client.post('/signup', data=dict(
        username="testtrainee",
        password="password",
        repassword="password",
        name="first last",
        phone=1234567890,
        usertype="trainee",
        lng=0,
        lat=0
    ), follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'Account was created!' not in returned_value.data
    assert b'Could not create account' not in returned_value.data
    assert b'Username was taken' in returned_value.data
    assert b'<form action="/signup" method="POST">' in returned_value.data

    trainee = g.database.get_trainee_by_username("testtrainee")
    trainer = g.database.get_trainer_by_username("testtrainer")

    clean_up(trainer, trainee)

    # POST with a username that was not taken, success, Trainee
    returned_value = client.post('/signup', data=dict(
        username="testtrainee",
        password="password",
        repassword="password",
        name="first last",
        phone=1234567890,
        usertype="trainee",
        lng=0,
        lat=0
    ), follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'Account was created!' in returned_value.data
    assert b'Could not create account' not in returned_value.data
    assert b'Username was taken' not in returned_value.data
    assert b'<form action="/signup" method="POST">' not in returned_value.data

    clean_up(trainer, trainee)

    # POST with a username that was not taken, success, Trainer
    returned_value = client.post('/signup', data=dict(
        username="testtrainer",
        password="password",
        repassword="password",
        name="first last",
        phone=1234567890,
        usertype="trainer",
        lng=0,
        lat=0
    ), follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'Account was created!' in returned_value.data
    assert b'Could not create account' not in returned_value.data
    assert b'Username was taken' not in returned_value.data
    assert b'<form action="/signup" method="POST">' not in returned_value.data

    clean_up(trainer, trainee)


def test_profile(client):
    """Testing the profile page"""
    # Get without a user
    returned_value = client.get('/profile/test', follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'login' in returned_value.data

    trainer = g.database.get_trainer_by_username("testtrainer")
    trainee = g.database.get_trainee_by_username("testtrainee")

    # Login
    login_as_testTrainee(client)

    # Check profile page.
    returned_value = client.get('/profile/testtrainee', follow_redirects=True)
    assert returned_value.status_code == 200
    assert bytes('Username: {}'.format(trainee.username),
                 'utf-8') in returned_value.data
    assert bytes('Name: {}'.format(trainee.name),
                 'utf-8') in returned_value.data
    assert bytes('Phone: {}'.format(trainee.phone),
                 'utf-8') in returned_value.data
    assert b'login' not in returned_value.data

    # Login
    login_as_testTrainer(client)

    # Check profile page.
    returned_value = client.get('/profile/testtrainer', follow_redirects=True)
    assert returned_value.status_code == 200
    assert bytes('Username: {}'.format(trainer.username),
                 'utf-8') in returned_value.data
    assert bytes('Name: {}'.format(trainer.name),
                 'utf-8') in returned_value.data
    assert bytes('Phone: {}'.format(trainer.phone),
                 'utf-8') in returned_value.data
    assert b'login' not in returned_value.data


def test_usersettings(client):
    """Testing the user settings page"""
    # Get without a user
    returned_value = client.get('/usersettings', follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'login' in returned_value.data

    # Login as trainee
    login_as_testTrainee(client)

    # Get id before change
    database_user_id = g.database.get_trainee_by_username("testtrainee")._id

    # Check profile page.
    returned_value = client.post('/usersettings', data=dict(
        username="testtrainee",
        password="newpassword",
        repassword="newpassword",
        name="another",
        phone="0987654321",
        lng=0,
        lat=0
    ), follow_redirects=True)
    assert returned_value.status_code == 200

    # Check database
    database_user = g.database.get_trainee_by_username("testtrainee")

    assert database_user._id == database_user_id
    assert database_user.username == 'testtrainee'
    assert database_user.password == password_sha256('newpassword')
    assert database_user.name == 'another'
    assert database_user.phone == '0987654321'

    # Login as trainer
    login_as_testTrainer(client)

    # Get id before change
    database_user_id = g.database.get_trainer_by_username("testtrainer")._id

    # Check profile page.
    returned_value = client.post('/usersettings', data=dict(
        username="testtrainer",
        password="newpassword",
        repassword="newpassword",
        name="another",
        phone="0987654321",
        lng=0,
        lat=0
    ), follow_redirects=True)
    assert returned_value.status_code == 200

    # Check database
    database_user = g.database.get_trainer_by_username("testtrainer")

    assert database_user._id == database_user_id
    assert database_user.username == 'testtrainer'
    assert database_user.password == password_sha256('newpassword')
    assert database_user.name == 'another'
    assert database_user.phone == '0987654321'

    # Checking alphaPattern
    for character in '!@#$%^&*()_+\\<>.':
        trainer = g.database.get_trainer_by_username("testtrainer")
        trainer.username = f"abc{character}"
        returned_value = client.post('/usersettings', data=dict(
            username=trainer.username,
            password=trainer.password,
            repassword=trainer.password,
            name=trainer.name,
            phone=trainer.phone
        ), follow_redirects=True)
        assert returned_value.status_code == 400

    for character in '!@#$%^&*()_+\\<>.':
        trainer = g.database.get_trainer_by_username("testtrainer")
        trainer.password = f"abc{character}"
        returned_value = client.post('/usersettings', data=dict(
            username=trainer.username,
            password=trainer.password,
            repassword=trainer.password,
            name=trainer.name,
            phone=trainer.phone
        ), follow_redirects=True)
        assert returned_value.status_code == 400

    for character in '!@#$%^&*()_+\\<>.':
        trainer = g.database.get_trainer_by_username("testtrainer")
        repassword = f"abc{character}"
        returned_value = client.post('/usersettings', data=dict(
            username=trainer.username,
            password=trainer.password,
            repassword=repassword,
            name=trainer.name,
            phone=trainer.phone
        ), follow_redirects=True)
        assert returned_value.status_code == 400

    for character in '!@#$%^&*()_+\\<>.':
        trainer = g.database.get_trainer_by_username("testtrainer")
        trainer.name = f"abc{character}"
        returned_value = client.post('/usersettings', data=dict(
            username=trainer.username,
            password=trainer.password,
            repassword=repassword,
            name=trainer.name,
            phone=trainer.phone
        ), follow_redirects=True)
        assert returned_value.status_code == 400

    for character in '!@#$%^&*()_+\\<>.':
        trainer = g.database.get_trainer_by_username("testtrainer")
        returned_value = client.post('/usersettings', data=dict(
            username=trainer.username,
            password=trainer.password,
            repassword=repassword,
            name=trainer.name,
            phone=trainer.phone
        ), follow_redirects=True)
        assert returned_value.status_code == 400

    for character in '!@#$%^&*()_+\\<>.a':
        trainer = g.database.get_trainer_by_username("testtrainer")
        trainer.phone = f"abc{character}"
        returned_value = client.post('/usersettings', data=dict(
            username=trainer.username,
            password=trainer.password,
            repassword=repassword,
            name=trainer.name,
            phone=trainer.phone
        ), follow_redirects=True)
        assert returned_value.status_code == 400


def test_logout(client):
    """Testing the logout page"""

    # Login
    login_as_testTrainee(client)

    # Logout with redirects on
    returned_value = client.get('/logout', follow_redirects=True)
    assert returned_value.status_code == 200
    assert g.user is None
    assert 'user_id' not in session

    # Login
    login_as_testTrainee(client)

    # Logout with redirects off
    returned_value = client.get('/logout', follow_redirects=False)
    assert returned_value.status_code == 302
    assert g.user is None
    assert 'user_id' not in session


def test_trainer_overview(client):
    """Testing the trainer overview page"""

    # Trainer Overview no user
    returned_value = client.get('/trainer_overview', follow_redirects=True)
    assert returned_value.status_code == 200
    assert g.user is None
    assert b'login' in returned_value.data

    # Login as Trainee
    login_as_testTrainee(client)

    # Trainer Overview as Trainee
    returned_value = client.get('/trainer_overview', follow_redirects=True)
    assert returned_value.status_code == 403
    assert type(g.user) == Trainee
    assert b'Page Forbidden' in returned_value.data

    # Login as Trainer
    login_as_testTrainer(client)

    trainee = g.database.get_trainee_by_username('testtrainee')
    trainer = g.database.get_trainer_by_username('testtrainer')

    g.database.mongo.trainer.update_one(
        {"_id": ObjectId(trainer._id)},
        {
            "$addToSet": {
                "trainees": ObjectId(trainee._id)
            }
        })

    invitation = g.database.mongo.invitation.insert_one({
        'sender': ObjectId(trainee._id),
        'recipient': ObjectId(trainer._id)
    })

    # Trainer Overview as Trainer
    returned_value = client.get('/trainer_overview', follow_redirects=True)
    assert returned_value.status_code == 200
    assert type(g.user) == Trainer
    assert b'/trainee_search' in returned_value.data
    assert b'/list_trainees' in returned_value.data

    g.database.mongo.invitation.delete_many({
        'sender': ObjectId(trainee._id)
    })


def test_list_trainees(client):
    """Testing the trainer list page"""

    # Trainer Overview no user
    returned_value = client.get('/list_trainees',
                                follow_redirects=True)
    assert returned_value.status_code == 200
    assert g.user is None
    assert b'login' in returned_value.data

    # Login as Trainee
    login_as_testTrainee(client)

    # Trainer Overview as Trainee
    returned_value = client.get('/list_trainees',
                                follow_redirects=True)
    assert returned_value.status_code == 403
    assert type(g.user) == Trainee
    assert b'Page Forbidden' in returned_value.data

    # Login as Trainer
    login_as_testTrainer(client)

    # Trainer Overview as Trainer
    returned_value = client.get('/list_trainees',
                                follow_redirects=True)
    assert returned_value.status_code == 200
    assert type(g.user) == Trainer
    assert b'No trainees found' in returned_value.data

    trainee = g.database.get_trainee_by_username('testtrainee')
    trainer = g.database.get_trainer_by_username('testtrainer')

    g.database.mongo.trainer.update_one(
        {"_id": ObjectId(trainer._id)},
        {
            "$addToSet": {
                "trainees": ObjectId(trainee._id)
            }
        })
    # Trainer Overview as Trainer
    returned_value = client.get('/list_trainees',
                                follow_redirects=True)
    assert returned_value.status_code == 200
    assert type(g.user) == Trainer
    assert b'No trainees found' not in returned_value.data


def test_trainee_overview(client):
    """Testing the trainer overview page"""

    # Trainer Overview no user
    returned_value = client.get('/trainee_overview', follow_redirects=True)
    assert returned_value.status_code == 200
    assert g.user is None
    assert b'login' in returned_value.data

    # Login as Trainee
    login_as_testTrainee(client)

    trainee = g.database.get_trainee_by_username('testtrainee')
    trainer = g.database.get_trainer_by_username('testtrainer')

    g.database.mongo.trainee.update_one(
        {"_id": ObjectId(trainee._id)},
        {
            "$addToSet": {
                "trainers": ObjectId(trainer._id)
            }
        })

    invitation = g.database.mongo.invitation.insert_one({
        'sender': ObjectId(trainer._id),
        'recipient': ObjectId(trainee._id)
    })

    # Trainee Overview as Trainee
    returned_value = client.get('/trainee_overview', follow_redirects=True)
    assert returned_value.status_code == 200
    assert type(g.user) == Trainee
    assert b'/trainer_search' in returned_value.data
    assert b'/list_trainers' in returned_value.data

    g.database.mongo.invitation.delete_many({
        'sender': ObjectId(trainer._id)
    })

    # Login as Trainer
    login_as_testTrainer(client)

    # Trainee Overview as Trainer
    returned_value = client.get('/trainee_overview',
                                follow_redirects=True)
    assert returned_value.status_code == 403
    assert type(g.user) == Trainer
    assert b'Page Forbidden' in returned_value.data


def test_trainer_search(client):
    """Test the /trainer_search page to add a trainer to a trainee"""
    returned_value = client.get('/trainer_search', follow_redirects=True)
    assert returned_value.status_code == 200
    assert g.user is None
    assert b'login' in returned_value.data

    login_as_testTrainer(client)
    returned_value = client.get('/trainer_search', follow_redirects=True)
    assert returned_value.status_code == 403
    assert type(g.user) == Trainer
    assert b'Page Forbidden' in returned_value.data

    login_as_testTrainee(client)
    returned_value = client.get('/trainer_search', follow_redirects=True)
    assert returned_value.status_code == 200
    assert type(g.user) == Trainee
    assert b'Overview' in returned_value.data
    assert b'Workouts' in returned_value.data
    assert b'Schedule' in returned_value.data
    assert b'Diets' in returned_value.data

    # Search for trainer with only first 3 letters
    returned_value = client.post('/trainer_search',
                                 data=dict(
                                     trainer_name=test_trainer.username[0:3]
                                 ), follow_redirects=True)
    assert returned_value.status_code == 200
    assert type(g.user) == Trainee
    assert bytes(test_trainer.username, 'utf-8') in returned_value.data
    assert bytes('/profile/%s' % test_trainer.username,
                 'utf-8') in returned_value.data
    assert b'Schedule' in returned_value.data
    assert b'Diets' in returned_value.data


def test_trainee_search(client):
    """Test the /trainee_search page to add a trainee to a trainer"""
    returned_value = client.get('/trainee_search', follow_redirects=True)
    assert returned_value.status_code == 200
    assert g.user is None
    assert b'login' in returned_value.data

    login_as_testTrainee(client)
    returned_value = client.get('/trainee_search', follow_redirects=True)
    assert returned_value.status_code == 403
    assert type(g.user) == Trainee
    assert b'Page Forbidden' in returned_value.data

    login_as_testTrainer(client)
    returned_value = client.get('/trainee_search', follow_redirects=True)
    assert returned_value.status_code == 200
    assert type(g.user) == Trainer
    assert b'Overview' in returned_value.data
    assert b'Workouts' in returned_value.data
    assert b'Schedule' in returned_value.data
    assert b'Diets' in returned_value.data

    # Search for trainer with only first 3 letters
    returned_value = client.post('/trainee_search',
                                 data=dict(
                                     trainee_name=test_trainee.username[0:3]
                                 ), follow_redirects=True)
    assert returned_value.status_code == 200
    assert type(g.user) == Trainer
    assert bytes(test_trainee.username, 'utf-8') in returned_value.data
    assert bytes('/profile/%s' % test_trainee.username,
                 'utf-8') in returned_value.data
    assert b'Schedule' in returned_value.data
    assert b'Diets' in returned_value.data


def test_add_trainer(client):
    """Testing the add_trainer page"""

    # Redirect to login page if not logged in
    returned_value = client.post('/add_trainer',
                                 data={
                                     'trainer_id': 0
                                 },
                                 follow_redirects=True)
    assert returned_value.status_code == 200
    assert g.user is None
    assert b'login' in returned_value.data

    login_as_testTrainer(client)

    # Get a 403 if logged in as trainer
    returned_value = client.post('/add_trainer',
                                 data={
                                     'trainer_id': 0
                                 },
                                 follow_redirects=True)
    assert returned_value.status_code == 403
    assert type(g.user) == Trainer
    assert b'Page Forbidden!' in returned_value.data

    login_as_testTrainee(client)

    # Add a trainer as a trainee
    trainer_id = g.database.get_trainer_by_username(test_trainer.username)._id
    returned_value = client.post('/add_trainer',
                                 data={
                                     'trainer_id': trainer_id
                                 },
                                 follow_redirects=True)
    assert returned_value.status_code == 204
    assert type(g.user) == Trainee

    returned_value = client.post('/add_trainer',
                                 data={
                                     'trainer_id': "123456789012345678901234"
                                 },
                                 follow_redirects=True)
    assert returned_value.status_code == 500
    assert type(g.user) == Trainee


def test_add_trainee(client):
    """Testing the add_trainee page"""

    # Redirect to login page if not logged in
    returned_value = client.post('/add_trainee',
                                 data={
                                     'trainer_id': 0
                                 },
                                 follow_redirects=True)
    assert returned_value.status_code == 200
    assert g.user is None
    assert b'login' in returned_value.data

    login_as_testTrainee(client)

    # Get a 403 if logged in as trainee
    returned_value = client.post('/add_trainee',
                                 data={
                                     'trainer_id': 0
                                 },
                                 follow_redirects=True)
    assert returned_value.status_code == 403
    assert type(g.user) == Trainee
    assert b'Page Forbidden!' in returned_value.data

    login_as_testTrainer(client)

    # Add a trainer as a trainer
    trainee_id = g.database.get_trainee_by_username(test_trainee.username)._id
    returned_value = client.post('/add_trainee',
                                 data={
                                     'trainee_id': trainee_id
                                 },
                                 follow_redirects=True)
    assert returned_value.status_code == 204
    assert type(g.user) == Trainer

    returned_value = client.post('/add_trainee',
                                 data={
                                     'trainee_id': "123456789012345678901234"
                                 },
                                 follow_redirects=True)
    assert returned_value.status_code == 500
    assert type(g.user) == Trainer


def test_list_trainers(client):
    """Testing the trainee overview page"""

    returned_value = client.get('/list_trainers',
                                follow_redirects=True)
    assert returned_value.status_code == 200
    assert g.user is None

    # Login as Trainee
    login_as_testTrainee(client)

    returned_value = client.get('/list_trainers',
                                follow_redirects=True)
    assert returned_value.status_code == 200
    assert type(g.user) == Trainee
    assert type(g.user) != Trainer

    trainee = g.database.get_trainee_by_username('testtrainee')
    trainer = g.database.get_trainer_by_username('testtrainer')

    g.database.mongo.trainee.update_one(
        {"_id": ObjectId(trainee._id)},
        {
            "$addToSet": {
                "trainers": ObjectId(trainer._id)
            }
        })

    returned_value = client.get('/list_trainers',
                                follow_redirects=True)
    assert returned_value.status_code == 200
    assert type(g.user) == Trainee
    assert b'No trainers found' not in returned_value.data

    login_as_testTrainer(client)
    returned_value = client.get('/list_trainers',
                                follow_redirects=True)
    assert returned_value.status_code == 403
    assert type(g.user) == Trainer
    assert b'Page Forbidden' in returned_value.data


def test_trainee_schedule(client):
    """Testing the trainer overview page"""

    # Trainer Overview no user
    returned_value = client.get('/schedule',
                                follow_redirects=True)
    assert returned_value.status_code == 200
    assert g.user is None

    # Login as Trainee
    login_as_testTrainee(client)

    # Trainee Overview as Trainee
    returned_value = client.get('/schedule',
                                follow_redirects=True)
    assert returned_value.status_code == 200
    assert type(g.user) == Trainee

    trainee = g.database.get_trainee_by_username('testtrainee')
    trainer = g.database.get_trainer_by_username('testtrainer')

    try:

        event = Event(
            _id=None,
            title='testEvent',
            creator_id=trainee._id,
            description='a description',
            date=datetime(2020, 3, 6),
            participant_id=trainer._id
        )

        g.database.mongo.event.delete_many({
            'title': event.title,
            'creator_id': ObjectId(trainee._id)
        })

        g.database.create_event(event)

        database_event = g.database.mongo.event.find_one({
            'title': event.title,
            'creator_id': ObjectId(trainee._id)
        })

        assert database_event is not None

        returned_value = client.get('/schedule',
                                    follow_redirects=True)
        assert returned_value.status_code == 200
        assert type(g.user) == Trainee
        assert bytes('{}'.format(event.title), 'utf-8') in returned_value.data
        assert bytes('{}'.format(event.date), 'utf-8') in returned_value.data

        login_as_testTrainer(client)

        # Trainer Overview as Trainer
        returned_value = client.get('/schedule',
                                    follow_redirects=True)
        assert returned_value.status_code == 200
        assert type(g.user) == Trainer
        assert bytes('{}'.format(event.title), 'utf-8') in returned_value.data
        assert bytes('{}'.format(event.date), 'utf-8') in returned_value.data

    finally:
        g.database.mongo.event.delete_many({
            'title': event.title,
            'creator_id': ObjectId(trainee._id)
        })


def test_add_event(client):

    # Trainer Overview no user
    returned_value = client.get('/add_event',
                                follow_redirects=True)
    assert returned_value.status_code == 200
    assert g.user is None
    assert b'login' in returned_value.data

    trainee = g.database.get_trainee_by_username('testtrainee')
    trainer = g.database.get_trainer_by_username('testtrainer')

    try:

        login_as_testTrainee(client)
        returned_value = client.get('/add_event',
                                    follow_redirects=True)
        assert type(g.user) is Trainee
        assert returned_value.status_code == 200

        returned_value = client.post('/add_event',
                                     data=dict(
                                         title='testEvent',
                                         description='a desc',
                                         date='2020-12-2',
                                         time='12:12',
                                         participant_id=trainer._id,
                                     ),
                                     follow_redirects=True)
        assert type(g.user) is Trainee
        assert returned_value.status_code == 200
        assert b'Created Event' in returned_value.data

        database_event = g.database.mongo.event.find_one({
            'title': 'testEvent',
            'creator_id': ObjectId(trainee._id)
        })

        assert database_event is not None

        login_as_testTrainer(client)
        returned_value = client.get('/add_event',
                                    follow_redirects=True)
        assert type(g.user) is Trainer
        assert returned_value.status_code == 200

        returned_value = client.post('/add_event',
                                     data=dict(
                                         title='testEvent',
                                         description='a desc',
                                         date='2020-12-2',
                                         time='12:12',
                                         participant_id=trainee._id,
                                     ),
                                     follow_redirects=True)
        assert type(g.user) is Trainer
        assert returned_value.status_code == 200
        assert b'Created Event' in returned_value.data

        database_event = g.database.mongo.event.find_one({
            'title': 'testEvent',
            'creator_id': ObjectId(trainer._id)
        })

        assert database_event is not None

    finally:
        g.database.mongo.event.delete_many({
            'title': 'testEvent',
            'creator_id': ObjectId(trainee._id)
        })


def test_display_event(client):
    # Trainer Overview no user
    returned_value = client.get('/event/123/123',
                                follow_redirects=True)
    assert returned_value.status_code == 200
    assert g.user is None
    assert b'login' in returned_value.data

    trainee = g.database.get_trainee_by_username('testtrainee')
    trainer = g.database.get_trainer_by_username('testtrainer')

    try:

        login_as_testTrainee(client)

        event = Event(
            _id=None,
            title='testEvent',
            creator_id=trainee._id,
            description='a description',
            date=datetime(2020, 3, 6),
            participant_id=trainer._id
        )

        g.database.mongo.event.delete_many({
            'title': event.title,
            'creator_id': ObjectId(trainee._id)
        })

        g.database.create_event(event)

        database_event = g.database.mongo.event.find_one({
            'title': event.title,
            'creator_id': ObjectId(trainee._id)
        })

        assert database_event is not None

        returned_value = client.get(f'/event/{trainee._id}/{event.title}',
                                    follow_redirects=True)
        assert type(g.user) is Trainee
        assert returned_value.status_code == 200
        assert bytes(''.format(event.title), 'utf-8') in returned_value.data
        assert bytes(''.format(event.description),
                     'utf-8') in returned_value.data
        assert bytes(''.format(event.date), 'utf-8') in returned_value.data

    finally:
        g.database.mongo.event.delete_many({
            'title': 'testEvent',
            'creator_id': ObjectId(trainee._id)
        })


def test_page_forbidden(client):
    """Testing the 403 page"""

    # Loggin in correctly
    login_as_testTrainee(client)

    # Trying to access restricted area as Trainee
    returned_value = client.get('/trainer_overview', follow_redirects=True)
    assert returned_value.status_code == 403
    assert b'Page Forbidden!' in returned_value.data


def test_page_not_found(client):
    """Testing the 404 page"""
    returned_value = client.get('/shouldnotexist', follow_redirects=True)
    assert returned_value.status_code == 404
    assert b'Page not found!' in returned_value.data


def test_page_bad_request(client):
    """Testing the 400 page"""
    # Login as Trainee
    returned_value = client.post('/login', data=dict(
        username="testtrainee",
    ), follow_redirects=True)
    assert returned_value.status_code == 400
    assert b'Could not log you in!' not in returned_value.data
    assert b'Bad Request!' in returned_value.data


def test_new_workout(client):
    """Testing the new workout page"""

    # Not logged in
    returned_value = client.get('/new_workout', follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'login' in returned_value.data
    assert g.user is None

    # Login as Trainee
    login_as_testTrainee(client)
    returned_value = client.get('/new_workout', follow_redirects=True)
    assert returned_value.status_code == 200
    assert type(g.user) == Trainee
    assert b'Difficulty' in returned_value.data
    assert b'Workout Name' in returned_value.data
    assert b'Type your workout description here' in returned_value.data
    assert b'Create Routine' in returned_value.data

    # Adding a workout as a trainer

    g.database.mongo.workout.delete_many({
        'creator_id': g.user._id
    })

    # With difficulty = novice
    new_workout = Workout(
        _id=None,
        creator_id=g.user._id,
        difficulty="novice",
        name="workout_test_one",
        about="This is a super cool description of what the workout is...\nwoo!",
        total_time="20",
        reps="10",
        miles="2",
        category="Cardio"
    )

    returned_value = client.post('/new_workout', data=dict(
        difficulty=new_workout.difficulty,
        name=new_workout.name,
        about=new_workout.about,
        total_time=new_workout.total_time,
        reps=new_workout.reps,
        miles=new_workout.miles,
        category=new_workout.category
    ), follow_redirects=True)
    assert b'Workout has been added!' in returned_value.data
    database_workout = g.database.get_workout_by_attributes(name="workout_test_one",
                                                            creator_id=g.user._id)
    new_workout._id = database_workout._id
    assert database_workout.as_dict() == new_workout.as_dict()

    returned_value = client.post('/new_workout', data=dict(
        difficulty=new_workout.difficulty,
        name=new_workout.name,
        about=new_workout.about,
        total_time=new_workout.total_time,
        reps=new_workout.reps,
        miles=new_workout.miles,
        category=new_workout.category
    ), follow_redirects=True)
    assert returned_value.status_code == 400
    assert b'Workout name already exists under your account!' in returned_value.data

    g.database.remove_workout(new_workout._id)

    # With difficulty = intermediate
    new_workout = Workout(
        _id=None,
        creator_id=g.user._id,
        difficulty="intermediate",
        name="workout_test_one",
        about="This is a super cool description of what the workout is...\nwoo!",
        total_time="20",
        reps="10",
        miles="2",
        category="Cardio"
    )

    returned_value = client.post('/new_workout', data=dict(
        difficulty=new_workout.difficulty,
        name=new_workout.name,
        about=new_workout.about,
        total_time=new_workout.total_time,
        reps=new_workout.reps,
        miles=new_workout.miles,
        category=new_workout.category
    ), follow_redirects=True)
    assert b'Workout has been added!' in returned_value.data
    database_workout = g.database.get_workout_by_attributes(name="workout_test_one",
                                                            creator_id=g.user._id)
    new_workout._id = database_workout._id
    assert database_workout.as_dict() == new_workout.as_dict()

    g.database.remove_workout(new_workout._id)

    # With difficulty = experienced
    new_workout = Workout(
        _id=None,
        creator_id=g.user._id,
        difficulty="experienced",
        name="workout_test_one",
        about="This is a super cool description of what the workout is...\nwoo!",
        total_time="20",
        reps="10",
        miles="2",
        category="Cardio"
    )

    returned_value = client.post('/new_workout', data=dict(
        difficulty=new_workout.difficulty,
        name=new_workout.name,
        about=new_workout.about,
        total_time=new_workout.total_time,
        reps=new_workout.reps,
        miles=new_workout.miles,
        category=new_workout.category
    ), follow_redirects=True)
    assert b'Workout has been added!' in returned_value.data
    database_workout = g.database.get_workout_by_attributes(name="workout_test_one",
                                                            creator_id=g.user._id)
    new_workout._id = database_workout._id
    assert database_workout.as_dict() == new_workout.as_dict()

    g.database.remove_workout(new_workout._id)

    # With difficulty = superstar
    new_workout = Workout(
        _id=None,
        creator_id=g.user._id,
        difficulty="superstar",
        name="workout_test_one",
        about="This is a super cool description of what the workout is...\nwoo!",
        total_time="20",
        reps="10",
        miles="2",
        category="Cardio"
    )

    returned_value = client.post('/new_workout', data=dict(
        difficulty=new_workout.difficulty,
        name=new_workout.name,
        about=new_workout.about,
        total_time=new_workout.total_time,
        reps=new_workout.reps,
        miles=new_workout.miles,
        category=new_workout.category
    ), follow_redirects=True)
    assert b'Workout has been added!' in returned_value.data
    database_workout = g.database.get_workout_by_attributes(name="workout_test_one",
                                                            creator_id=g.user._id)
    new_workout._id = database_workout._id
    assert database_workout.as_dict() == new_workout.as_dict()
    g.database.remove_workout(new_workout._id)

    # Login as Trainer
    login_as_testTrainer(client)
    returned_value = client.get('/new_workout', follow_redirects=True)
    assert returned_value.status_code == 200
    assert type(g.user) == Trainer
    assert b'Difficulty' in returned_value.data
    assert b'Workout Name' in returned_value.data
    assert b'Type your workout description here' in returned_value.data
    assert b'Create Routine' in returned_value.data


def test_search_workout(client):
    """Testing the search workout page"""

    # Not logged in
    returned_value = client.get('/search_workout', follow_redirects=True)
    assert returned_value.status_code == 200

    trainee = g.database.get_trainee_by_username('testtrainee')
    trainer = g.database.get_trainer_by_username('testtrainer')

    try:

        # Login as Trainee
        login_as_testTrainee(client)
        sleep(.5)
        returned_value = client.get('/search_workout', follow_redirects=True)
        assert returned_value.status_code == 200

        login_as_testTrainee(client)

        workoutTest = Workout(
            _id=None,
            creator_id=trainer._id,
            name="testWorkout",
            difficulty="easy",
            about="2 Pushups, 1 Jumping Jack",
            total_time="20",
            reps="10",
            miles="2",
            category="Cardio"
        )

        g.database.add_workout(workoutTest)
        database_workout = g.database.get_all_workout_by_attributes(name=workoutTest.name,
                                                                    creator_id=trainer._id)

        login_as_testTrainer(client)
        sleep(.5)
        returned_value = client.get('/search_workout',
                                    follow_redirects=True)
        assert returned_value.status_code == 200
        sleep(.5)
        returned_value = client.post('/search_workout',
                                     data=dict(
                                         search_workout="workoutTest"
                                     ), follow_redirects=True)
    finally:
        g.database.mongo.workout.delete_many({
            'creator_id': ObjectId(trainee._id)
        })
        g.database.mongo.workout.delete_many({
            'creator_id': ObjectId(trainer._id)
        })


def test_workout(client):
    """Testing the workout page"""
    # Not logged in
    returned_value = client.get('/workout/adjr/00000', follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'login' in returned_value.data
    assert g.user is None

    trainee = g.database.get_trainee_by_username('testtrainee')
    trainer = g.database.get_trainer_by_username('testtrainer')

    workoutTest = Workout(
        _id=None,
        creator_id=trainer._id,
        name="testWorkout",
        difficulty="easy",
        about="2 Pushups, 1 Jumping Jack",
        total_time="20",
        reps="10",
        miles="2",
        category="Cardio"
    )

    g.database.add_workout(workoutTest)
    database_workout = g.database.get_workout_by_attributes(name=workoutTest.name,
                                                            creator_id=trainer._id)

    login_as_testTrainer(client)
    returned_value = client.get(f'/workout/{trainer._id}/{database_workout.name}',
                                follow_redirects=True)
    assert returned_value.status_code == 200
    assert bytes("{}".format(database_workout.name),
                 "utf-8") in returned_value.data
    assert bytes("{}".format(database_workout.difficulty),
                 "utf-8") in returned_value.data
    assert bytes("{}".format(database_workout.about),
                 "utf-8") in returned_value.data

    returned_value = client.post(f'/workout/{trainer._id}/{database_workout.name}',
                                 data=dict(
                                     completed='false',
                                     total_time='20',
                                     reps='10',
                                     miles='2',
                                     category='Cardio'
                                 ),
                                 follow_redirects=True)
    assert returned_value.status_code == 400

    # Complete an Easy workout
    returned_value = client.post(f'/workout/{trainer._id}/{database_workout.name}',
                                 data=dict(
                                     completed='true',
                                     total_time='20',
                                     reps='10',
                                     miles='2',
                                     category='Cardio'
                                 ),
                                 follow_redirects=True)
    trainer = g.database.get_trainer_by_username('testtrainer')
    database_workout = g.database.get_workout_by_attributes(name=workoutTest.name,
                                                            creator_id=trainer._id)
    assert returned_value.status_code == 200
    assert trainer is not None
    assert trainer.exp > 0
    assert database_workout.is_complete is True
    g.database.mongo.trainer.update_one(
        {"_id": ObjectId(trainer._id)},
        {
            "$set": {
                "exp": 0
            }
        })
    g.database.mongo.workout.update_one(
        {"_id": ObjectId(database_workout._id)},
        {
            "$set": {
                "is_complete": False
            }
        })

    # Complete an Medium workout
    g.database.mongo.workout.update_one(
        {"_id": ObjectId(database_workout._id)},
        {
            "$set": {
                "difficulty": "medium"
            }
        })
    returned_value = client.post(f'/workout/{trainer._id}/{database_workout.name}',
                                 data=dict(
                                     completed='true',
                                     total_time='20',
                                     reps='10',
                                     miles='2',
                                     category='Cardio'
                                 ),
                                 follow_redirects=True)
    trainer = g.database.get_trainer_by_username('testtrainer')
    database_workout = g.database.get_workout_by_attributes(name=workoutTest.name,
                                                            creator_id=trainer._id)
    assert returned_value.status_code == 200
    assert trainer is not None
    assert trainer.exp > 0
    assert database_workout.is_complete is True
    g.database.mongo.trainer.update_one(
        {"_id": ObjectId(trainer._id)},
        {
            "$set": {
                "exp": 0
            }
        })
    g.database.mongo.workout.update_one(
        {"_id": ObjectId(database_workout._id)},
        {
            "$set": {
                "is_complete": False
            }
        })

    # Complete an Hard workout
    g.database.mongo.workout.update_one(
        {"_id": ObjectId(database_workout._id)},
        {
            "$set": {
                "difficulty": "hard"
            }
        })
    returned_value = client.post(f'/workout/{trainer._id}/{database_workout.name}',
                                 data=dict(
                                     completed='true',
                                     total_time='20',
                                     reps='10',
                                     miles='2',
                                     category='Cardio'
                                 ),
                                 follow_redirects=True)
    trainer = g.database.get_trainer_by_username('testtrainer')
    database_workout = g.database.get_workout_by_attributes(name=workoutTest.name,
                                                            creator_id=trainer._id)
    assert returned_value.status_code == 200
    assert trainer is not None
    assert trainer.exp > 0
    assert database_workout.is_complete is True
    g.database.mongo.trainer.update_one(
        {"_id": ObjectId(trainer._id)},
        {
            "$set": {
                "exp": 0
            }
        })
    g.database.mongo.workout.update_one(
        {"_id": ObjectId(database_workout._id)},
        {
            "$set": {
                "is_complete": False
            }
        })

    # Complete an insane workout
    g.database.mongo.workout.update_one(
        {"_id": ObjectId(database_workout._id)},
        {
            "$set": {
                "difficulty": "insane"
            }
        })
    returned_value = client.post(f'/workout/{trainer._id}/{database_workout.name}',
                                 data=dict(
                                     completed='true',
                                     total_time='20',
                                     reps='10',
                                     miles='2',
                                     category='Cardio'
                                 ),
                                 follow_redirects=True)
    trainer = g.database.get_trainer_by_username('testtrainer')
    database_workout = g.database.get_workout_by_attributes(name=workoutTest.name,
                                                            creator_id=trainer._id)
    assert returned_value.status_code == 200
    assert trainer is not None
    assert trainer.exp > 0
    assert database_workout.is_complete is True
    g.database.mongo.trainer.update_one(
        {"_id": ObjectId(trainer._id)},
        {
            "$set": {
                "exp": 0
            }
        })
    g.database.mongo.workout.update_one(
        {"_id": ObjectId(database_workout._id)},
        {
            "$set": {
                "is_complete": False
            }
        })

    # Test if trainee can complete a workout
    login_as_testTrainee(client)
    workoutTest.creator_id = trainee._id
    g.database.add_workout(workoutTest)

    returned_value = client.post(f'/workout/{trainee._id}/{database_workout.name}',
                                 data=dict(
                                     completed='true',
                                     total_time='20',
                                     reps='10',
                                     miles='2',
                                     category='Cardio'
                                 ),
                                 follow_redirects=True)
    trainee = g.database.get_trainee_by_username('testtrainee')
    database_workout = g.database.get_workout_by_attributes(name=workoutTest.name,
                                                            creator_id=trainee._id)
    assert returned_value.status_code == 200
    assert trainee is not None
    assert trainee.exp > 0
    assert database_workout.is_complete is True
    g.database.mongo.trainee.update_one(
        {"_id": ObjectId(trainee._id)},
        {
            "$set": {
                "exp": 0
            }
        })
    g.database.mongo.workout.update_one(
        {"_id": ObjectId(database_workout._id)},
        {
            "$set": {
                "is_complete": False
            }
        })

    g.database.remove_workout(database_workout._id)
    returned_value = client.get(f'/workout/{trainer._id}/zebra',
                                follow_redirects=True)
    assert returned_value.status_code == 404


def test_workout_overview(client):
    """Testing the workout overview page"""

    # Not logged in
    returned_value = client.get('/workout_overview', follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'login' in returned_value.data
    assert g.user is None

    # Login as Trainee
    login_as_testTrainee(client)

    returned_value = client.get('/workout_overview', follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'Create a new workout routine.' in returned_value.data
    assert b'Search for workout routine.' in returned_value.data
    assert b'Your created workouts.' in returned_value.data

    # Login as Trainer
    login_as_testTrainer(client)

    returned_value = client.get('/workout_overview', follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'Create a new workout routine.' in returned_value.data
    assert b'Search for workout routine.' in returned_value.data
    assert b'Your created workouts.' in returned_value.data


def test_workout_list(client):
    """Testing the workout list page"""

    try:
        # Not logged in
        returned_value = client.get('/workout_list', follow_redirects=True)
        assert returned_value.status_code == 200
        assert b'login' in returned_value.data
        assert g.user is None

        login_as_testTrainer(client)
        returned_value = client.get('/workout_list', follow_redirects=True)
        assert returned_value.status_code == 200
        assert b'You have no created workouts' in returned_value.data
        assert type(g.user) is Trainer

        login_as_testTrainee(client)
        trainee = g.database.get_trainee_by_username(test_trainee.username)
        workout = g.database.add_workout(Workout(
            _id=None,
            creator_id=trainee._id,
            name="testWorkout",
            difficulty="expert",
            about="This is an about",
            total_time="20",
            reps="10",
            miles="2",
            category="Cardio"
        ))

        database_workout = g.database.mongo.workout.find_one({
            'creator_id': ObjectId(trainee._id),
            'name': "testWorkout"
        })
        returned_value = client.get('/workout_list', follow_redirects=True)
        assert returned_value.status_code == 200
        assert bytes('{}'.format(database_workout['name']),
                     'utf-8') in returned_value.data
        assert type(g.user) is Trainee

    finally:
        database_workout = g.database.mongo.workout.find_one({
            'creator_id': ObjectId(trainee._id),
            'name': "testWorkout"
        })
        if database_workout is not None:
            trainee = g.database.get_trainee_by_username(test_trainee.username)
            g.database.mongo.workout.delete_many({
                'name': "testWorkout",
                'creator_id': ObjectId(trainee._id)
            })


def test_delete_user(client):
    """Testing the delete user route"""

    # Not logged in
    returned_value = client.get('/delete', follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'login' in returned_value.data

    # login as testTrainee
    login_as_testTrainee(client)

    returned_value = client.get('/delete', follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'Delete Account' in returned_value.data

    # delete testTrainee
    returned_value = client.post(
        '/delete', data={'confirmation': 'true'}, follow_redirects=True)
    assert returned_value.status_code == 200
    assert g.user is None
    assert 'user_id' not in session
    assert g.database.get_trainee_by_username("testtrainee") is None

    # login as testTrainer
    login_as_testTrainer(client)

    # delete testTrainer
    returned_value = client.post(
        '/delete', data={'confirmation': 'true'}, follow_redirects=True)
    assert returned_value.status_code == 200
    assert g.user is None
    assert 'user_id' not in session
    assert g.database.get_trainer_by_username("testtrainer") is None


def test_delete_user_without_confirmation(client):
    """Reseting the environment and deleting without a confirmation should return a 500"""
    login_as_testTrainer(client)
    returned_value = client.post('/delete',
                                 data={'confirmation': 'false'},
                                 follow_redirects=True)
    assert returned_value.status_code == 500


def test_remove_added_user(client):
    # Not logged in
    returned_value = client.post('/remove_added_user', follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'login' in returned_value.data
    assert g.user is None

    login_as_testTrainee(client)

    returned_value = client.post('/remove_added_user',
                                 data={
                                     'confirmation': 'false',
                                     'user_id': 'abc'
                                 },
                                 follow_redirects=True)
    assert returned_value.status_code == 500

    returned_value = client.post('/remove_added_user',
                                 data={
                                     'confirmation': 'true',
                                     'user_id': ''
                                 },
                                 follow_redirects=True)
    assert returned_value.status_code == 500

    trainee = g.database.get_trainee_by_username("testtrainee")
    trainer = g.database.get_trainer_by_username("testtrainer")

    # Remove trainer from trainee

    g.database.mongo.trainee.update_one(
        {"_id": ObjectId(trainee._id)},
        {
            "$addToSet": {
                "trainers": ObjectId(trainer._id)
            }
        })

    assert ObjectId(trainer._id) in g.database.mongo.trainee.find_one({
        '_id': ObjectId(trainee._id)
    })['trainers']

    returned_value = client.post('/remove_added_user',
                                 data={
                                     'confirmation': 'true',
                                     'user_id': str(trainer._id)
                                 },
                                 follow_redirects=True)
    assert returned_value.status_code == 204

    # Remove trainee from trainer
    login_as_testTrainer(client)

    g.database.mongo.trainer.update_one(
        {"_id": ObjectId(trainer._id)},
        {
            "$addToSet": {
                "trainees": ObjectId(trainee._id)
            }
        })

    assert ObjectId(trainee._id) in g.database.mongo.trainer.find_one({
        '_id': ObjectId(trainer._id)
    })['trainees']

    returned_value = client.post('/remove_added_user',
                                 data={
                                     'confirmation': 'true',
                                     'user_id': str(trainee._id)
                                 },
                                 follow_redirects=True)
    assert returned_value.status_code == 204

    # User not found


def test_invitations(client):
    returned_value = client.get('/invitations', follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'login' in returned_value.data
    assert g.user is None

    login_as_testTrainee(client)

    try:

        trainee = g.database.get_trainee_by_username('testtrainee')
        trainer = g.database.get_trainer_by_username('testtrainer')
        invitation = g.database.mongo.invitation.insert_one({
            'sender': ObjectId(trainer._id),
            'recipient': ObjectId(trainee._id)
        })

        returned_value = client.get('/invitations', follow_redirects=True)
        assert returned_value.status_code == 200
        assert type(g.user) is Trainee
        assert bytes('{}'.format(invitation.inserted_id),
                     'utf-8') in returned_value.data
    finally:
        g.database.mongo.invitation.delete_many({
            'sender': ObjectId(trainer._id),
            'recipient': ObjectId(trainee._id)
        })


def test_accept_invitation(client):
    returned_value = client.post('/accept_invitation',
                                 data={'confirmation': 'true'},
                                 follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'login' in returned_value.data
    assert g.user is None

    login_as_testTrainee(client)

    try:

        trainee = g.database.get_trainee_by_username('testtrainee')
        trainer = g.database.get_trainer_by_username('testtrainer')
        invitation = g.database.mongo.invitation.insert_one({
            'sender': ObjectId(trainer._id),
            'recipient': ObjectId(trainee._id)
        })

        returned_value = client.post('/accept_invitation',
                                     data={
                                         'confirmation': 'false',
                                         'invitation_id': '000000000000000000000000'
                                     },
                                     follow_redirects=True)
        assert returned_value.status_code == 500
        assert type(g.user) is Trainee

        returned_value = client.post('/accept_invitation',
                                     data={
                                         'confirmation': 'true',
                                         'invitation_id': str('000000000000000000000000')
                                     },
                                     follow_redirects=True)

        assert returned_value.status_code == 500

        returned_value = client.post('/accept_invitation',
                                     data={
                                         'confirmation': 'true',
                                         'invitation_id': str(invitation.inserted_id)
                                     },
                                     follow_redirects=True)
        assert returned_value.status_code == 204
        assert type(g.user) is Trainee
        assert g.database.mongo.invitation.find_one({
            'recipient': ObjectId(trainer._id)
        }) is None
        assert ObjectId(trainer._id) in g.database.mongo.trainee.find_one({
            '_id': ObjectId(trainee._id)
        })['trainers']
        assert ObjectId(trainee._id) in g.database.mongo.trainer.find_one({
            '_id': ObjectId(trainer._id)
        })['trainees']

    finally:
        g.database.mongo.invitation.delete_many({
            'sender': ObjectId(trainer._id),
            'recipient': ObjectId(trainee._id)
        })
