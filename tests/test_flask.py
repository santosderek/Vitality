import pytest
import unittest
from flask import g, session
from vitality import create_app
from vitality.database import Database, password_sha256
from vitality.trainee import Trainee
from vitality.trainer import Trainer

test_trainee = Trainee(
    _id=None,
    username="testTrainee",
    password="password",
    name="first last",
    location="Earth",
    phone=1234567890
)

test_trainer = Trainer(
    _id=None,
    username="testTrainer",
    password="password",
    name="first last",
    location="Earth",
    phone=1234567890
)


def login_as_testTrainee(client):
    """Login as testTrainee"""
    returned_value = client.post('/login', data=dict(
        username="testTrainee",
        password="password"
    ), follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'Could not log you in!' not in returned_value.data
    assert b'See Trainers' in returned_value.data
    assert b'Workouts' in returned_value.data
    assert b'Schedule' in returned_value.data


def login_as_testTrainer(client):
    """Login as testTrainer"""
    returned_value = client.post('/login', data=dict(
        username="testTrainer",
        password="password"
    ), follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'Could not log you in!' not in returned_value.data
    assert b'See Trainees' in returned_value.data
    assert b'Workouts' in returned_value.data
    assert b'Schedule' in returned_value.data


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    database = Database(app)

    def setup():
        """ Code run after client has been used """
        teardown()

        database.add_trainer(test_trainer)
        database.add_trainee(test_trainee)

    def teardown():
        """ Code run after client has been used """
        while database.get_trainee_by_username("testTrainee"):
            database.remove_trainee(
                database.get_trainee_by_username("testTrainee")._id)

        while database.get_trainer_by_username("testTrainer"):
            database.remove_trainer(
                database.get_trainer_by_username("testTrainer")._id)

    with app.test_client() as client:
        with app.app_context():
            setup()
            yield client
            teardown()


def test_home(client):
    """Testing the home page"""
    returned_value = client.get('/', follow_redirects=True)
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
    assert b'See Trainers' not in returned_value.data
    assert b'Username' in returned_value.data
    assert b'Password' in returned_value.data
    assert b'Login</button>' in returned_value.data
    assert b'Remember me</label>' in returned_value.data


def test_signup(client):
    """Testing the sign up page"""
    # Get without a user
    returned_value = client.get('/signup', follow_redirects=True)
    assert returned_value.status_code == 200

    # POST with a wrong password combination
    returned_value = client.post('/signup', data=dict(
        username="testTrainee",
        password="password",
        repassword="repassword",
        name="first last",
        location="Earth",
        phone=1234567890,
        usertype="trainee"
    ), follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'Account was created!' not in returned_value.data
    assert b'Could not create account' in returned_value.data
    assert b'Username was taken' not in returned_value.data
    assert b'<form action="/signup" method="POST">' in returned_value.data

    # POST with a wrong usertype
    returned_value = client.post('/signup', data=dict(
        username="testTrainee",
        password="password",
        repassword="password",
        name="first last",
        location="Earth",
        phone=1234567890,
        usertype="notausertype"
    ), follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'Account was created!' not in returned_value.data
    assert b'Could not create account' in returned_value.data
    assert b'Username was taken' not in returned_value.data
    assert b'<form action="/signup" method="POST">' in returned_value.data

    # POST with a username that was taken
    returned_value = client.post('/signup', data=dict(
        username="testTrainee",
        password="password",
        repassword="password",
        name="first last",
        location="Earth",
        phone=1234567890,
        usertype="trainee"
    ), follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'Account was created!' not in returned_value.data
    assert b'Could not create account' not in returned_value.data
    assert b'Username was taken' in returned_value.data
    assert b'<form action="/signup" method="POST">' in returned_value.data

    if g.database.get_trainee_by_username("testTrainee"):
        g.database.remove_trainee(
            g.database.get_trainee_by_username("testTrainee")._id)

    # POST with a username that was not taken, success
    returned_value = client.post('/signup', data=dict(
        username="testTrainee",
        password="password",
        repassword="password",
        name="first last",
        location="Earth",
        phone=1234567890,
        usertype="trainee"
    ), follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'Account was created!' in returned_value.data
    assert b'Could not create account' not in returned_value.data
    assert b'Username was taken' not in returned_value.data
    assert b'<form action="/signup" method="POST">' not in returned_value.data

    if g.database.get_trainee_by_username("testTrainee"):
        g.database.remove_trainee(
            g.database.get_trainee_by_username("testTrainee")._id)

    # POST with a username that was not taken, success
    returned_value = client.post('/signup', data=dict(
        username="testTrainee",
        password="password",
        repassword="password",
        name="first last",
        location="Earth",
        phone=1234567890,
        usertype="trainer"
    ), follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'Account was created!' in returned_value.data
    assert b'Could not create account' not in returned_value.data
    assert b'Username was taken' not in returned_value.data
    assert b'<form action="/signup" method="POST">' not in returned_value.data

    if g.database.get_trainer_by_username("testTrainee"):
        g.database.remove_trainer(
            g.database.get_trainer_by_username("testTrainee")._id)


def test_profile(client):
    """Testing the profile page"""
    # Get without a user
    returned_value = client.get('/profile/test', follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'login' in returned_value.data

    # Login
    login_as_testTrainee(client)

    # Check profile page.
    returned_value = client.get('/profile/testTrainee', follow_redirects=True)
    assert returned_value.status_code == 200
    assert b'Username: testTrainee' in returned_value.data
    assert b'Name: first last' in returned_value.data
    assert b'Phone: 1234567890' in returned_value.data
    assert b'Location: Earth' in returned_value.data
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
    database_user_id = g.database.get_trainee_by_username("testTrainee")._id

    # Check profile page.
    returned_value = client.post('/usersettings', data=dict(
        username="testTrainee",
        password="newpassword",
        repassword="newpassword",
        name="another",
        location="Venus",
        phone="0987654321"
    ), follow_redirects=True)
    assert returned_value.status_code == 200

    # Check database
    database_user = g.database.get_trainee_by_username("testTrainee")

    assert database_user._id == database_user_id
    assert database_user.username == 'testTrainee'
    assert database_user.password == password_sha256('newpassword')
    assert database_user.name == 'another'
    assert database_user.location == 'Venus'
    assert database_user.phone == '0987654321'

    # Login as trainer
    login_as_testTrainer(client)

    # Get id before change
    database_user_id = g.database.get_trainer_by_username("testTrainer")._id

    # Check profile page.
    returned_value = client.post('/usersettings', data=dict(
        username="testTrainer",
        password="newpassword",
        repassword="newpassword",
        name="another",
        location="Venus",
        phone="0987654321"
    ), follow_redirects=True)
    assert returned_value.status_code == 200

    # Check database
    database_user = g.database.get_trainer_by_username("testTrainer")

    assert database_user._id == database_user_id
    assert database_user.username == 'testTrainer'
    assert database_user.password == password_sha256('newpassword')
    assert database_user.name == 'another'
    assert database_user.location == 'Venus'
    assert database_user.phone == '0987654321'


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

    # Trainer Overview as Trainer
    returned_value = client.get('/trainer_overview', follow_redirects=True)
    assert returned_value.status_code == 200
    assert type(g.user) == Trainer


def test_trainer_list_trainees(client):
    """Testing the trainer list page"""

    # Trainer Overview no user
    returned_value = client.get('/trainer_list_trainees',
                                follow_redirects=True)
    assert returned_value.status_code == 200
    assert g.user is None
    assert b'login' in returned_value.data

    # Login as Trainee
    login_as_testTrainee(client)

    # Trainer Overview as Trainee
    returned_value = client.get('/trainer_list_trainees',
                                follow_redirects=True)
    assert returned_value.status_code == 403
    assert type(g.user) == Trainee
    assert b'Page Forbidden' in returned_value.data

    # Login as Trainer
    login_as_testTrainer(client)

    # Trainer Overview as Trainer
    returned_value = client.get('/trainer_list_trainees',
                                follow_redirects=True)
    assert returned_value.status_code == 200
    assert type(g.user) == Trainer
    print(returned_value.data)
    assert b'No trainees found' in returned_value.data


def test_trainer_schedule(client):
    """Testing the trainer schedule page"""

    # Trainer Overview no user
    returned_value = client.get('/trainer_schedule', follow_redirects=True)
    assert returned_value.status_code == 200
    assert g.user is None
    assert b'login' in returned_value.data

    # Login as Trainee
    login_as_testTrainee(client)

    # Trainer Overview as Trainee
    returned_value = client.get('/trainer_schedule', follow_redirects=True)
    assert returned_value.status_code == 403
    assert type(g.user) == Trainee

    # Login as Trainer
    login_as_testTrainer(client)

    # Trainer Overview as Trainer
    returned_value = client.get('/trainer_schedule',
                                follow_redirects=True)
    assert returned_value.status_code == 200
    assert type(g.user) == Trainer
    assert b'Schedule...' in returned_value.data


def test_trainee_overview(client):
    """Testing the trainer overview page"""

    # Trainer Overview no user
    returned_value = client.get('/trainee_overview', follow_redirects=True)
    assert returned_value.status_code == 200
    assert g.user is None
    assert b'login' in returned_value.data

    # Login as Trainee
    login_as_testTrainee(client)

    # Trainee Overview as Trainee
    returned_value = client.get('/trainee_overview', follow_redirects=True)
    assert returned_value.status_code == 200
    assert type(g.user) == Trainee

    # Login as Trainer
    login_as_testTrainer(client)

    # Trainee Overview as Trainer
    returned_value = client.get('/trainee_overview',
                                follow_redirects=True)
    assert returned_value.status_code == 403
    assert type(g.user) == Trainer
    assert b'Page Forbidden' in returned_value.data


def test_trainee_add_trainer(client):
    """Test the /trainee_add_trianer page to add a trainer to a trainee"""
    returned_value = client.get('/trainee_add_trainer', follow_redirects=True)
    assert returned_value.status_code == 200
    assert g.user is None
    assert b'login' in returned_value.data

    login_as_testTrainer(client)
    returned_value = client.get('/trainee_add_trainer', follow_redirects=True)
    assert returned_value.status_code == 403
    assert type(g.user) == Trainer
    assert b'Page Forbidden' in returned_value.data

    login_as_testTrainee(client)
    returned_value = client.get('/trainee_add_trainer', follow_redirects=True)
    assert returned_value.status_code == 200
    assert type(g.user) == Trainee
    assert b'Overview' in returned_value.data
    assert b'Workouts' in returned_value.data
    assert b'Schedule' in returned_value.data
    assert b'Diets' in returned_value.data

    # Search for trainer with only first 3 letters
    login_as_testTrainee(client)
    returned_value = client.post('/trainee_add_trainer', data=dict(
        trainer_name=test_trainer.username[0:3]
    ), follow_redirects=True)
    assert returned_value.status_code == 200
    assert type(g.user) == Trainee
    assert bytes(test_trainer.username, 'utf-8') in returned_value.data
    assert bytes('/profile/%s' % test_trainer.username,
                 'utf-8') in returned_value.data
    assert b'Schedule' in returned_value.data
    assert b'Diets' in returned_value.data

    # TODO: need to add checks to see if trainer gets added to trainee list


def test_trainee_list_trainers(client):
    """Testing the trainer overview page"""

    # Trainer Overview no user
    returned_value = client.get('/trainee_list_trainers',
                                follow_redirects=True)
    assert returned_value.status_code == 200
    assert g.user is None

    # Login as Trainee
    login_as_testTrainee(client)

    # Trainer Overview as Trainee
    returned_value = client.get('/trainee_list_trainers',
                                follow_redirects=True)
    assert returned_value.status_code == 200
    assert type(g.user) == Trainee
    assert type(g.user) != Trainer

    # Login as Trainer
    login_as_testTrainer(client)

    # Trainee Overview as Trainer
    returned_value = client.get('/trainee_list_trainers',
                                follow_redirects=True)
    assert returned_value.status_code == 403
    assert type(g.user) == Trainer
    assert b'Page Forbidden' in returned_value.data


def test_trainee_schedule(client):
    """Testing the trainer overview page"""

    # Trainer Overview no user
    returned_value = client.get('/trainee_schedule',
                                follow_redirects=True)
    assert returned_value.status_code == 200
    assert g.user is None

    # Login as Trainee
    login_as_testTrainee(client)

    # Trainee Overview as Trainee
    returned_value = client.get('/trainee_schedule',
                                follow_redirects=True)
    assert returned_value.status_code == 200
    assert type(g.user) == Trainee

    login_as_testTrainer(client)

    # Trainee Overview as Trainee
    returned_value = client.get('/trainee_schedule',
                                follow_redirects=True)
    assert returned_value.status_code == 403
    assert type(g.user) == Trainer
    assert b'Page Forbidden' in returned_value.data


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
        username="testTrainee",
    ), follow_redirects=True)
    assert returned_value.status_code == 400
    assert b'Could not log you in!' not in returned_value.data
    assert b'Bad Request!' in returned_value.data


def test_new_workout(client):
    """Testing the new workout page"""

    # Not logged in
    returned_value = client.get('/new_workout', follow_redirects=True)
    assert returned_value.status_code == 200

    # Login as Trainee
    login_as_testTrainee(client)

    returned_value = client.get('/new_workout', follow_redirects=True)
    assert returned_value.status_code == 200

    # TODO: need to test post requests


def test_search_workout(client):
    """Testing the search workout page"""

    # Not logged in
    returned_value = client.get('/search_workout', follow_redirects=True)
    assert returned_value.status_code == 200

    # Login as Trainee
    login_as_testTrainee(client)

    returned_value = client.get('/search_workout', follow_redirects=True)
    assert returned_value.status_code == 200

    login_as_testTrainee(client)

    # TODO: need to test post requests


@pytest.mark.skip(reason="no way of currently testing if Trianer can login")
def test_workout(client):
    """Testing the search workout page"""

    # TODO: Need to create a workout and add to database then check
    # Not logged in
    returned_value = client.get('/workout/', follow_redirects=True)
    assert returned_value.status_code == 200

    # Login as Trainee
    login_as_testTrainee(client)

    returned_value = client.get('/workout', follow_redirects=True)
    assert returned_value.status_code == 200

    # TODO: need to test post requests


@pytest.mark.skip(reason="no way of currently testing if Trianer can login")
def test_workout_overview(client):
    """Testing the search workout page"""

    # TODO: Need to create a workout and add to database then check
    # Not logged in
    returned_value = client.get('/workout_overview', follow_redirects=True)
    assert returned_value.status_code == 200

    # Login as Trainee
    login_as_testTrainee(client)

    returned_value = client.get('/workout_overview', follow_redirects=True)
    assert returned_value.status_code == 200

    # TODO: need to test post requests


def test_workout_list(client):
    """Testing the workout list page"""

    # Not logged in
    returned_value = client.get('/workout_list', follow_redirects=True)
    assert returned_value.status_code == 200

    # Login as Trainee
    login_as_testTrainee(client)

    returned_value = client.get('/workout_list', follow_redirects=True)
    assert returned_value.status_code == 200

    # TODO: need to test post requests
