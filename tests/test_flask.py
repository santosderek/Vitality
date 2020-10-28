import unittest
from vitality import create_app
from vitality.database import Database
from vitality.user import User

class TestFlask(unittest.TestCase):

    def setUp(self):
        # Create the Flask app and database
        self.app_original = create_app()
        self.database = Database(self.app_original)

        # After database, then make self.app the flask test_client class
        self.app_test = self.app_original.test_client()

        # Adding test user
        if self.database.get_by_username("test"):
            self.database.remove_user(
                self.database.get_by_username("test")['_id'])
        test_user = User(
            None,
            username="test",
            password="password",
            firstname="first",
            lastname="last",
            location="Earth",
            phone=1234567890
        )
        self.database.add_user(test_user)

    def tearDown(self):
        if self.database.get_by_username("test"):
            self.database.remove_user(
                self.database.get_by_username("test")['_id'])

    def test_home(self):
        returned_value = self.app_test.get('/', follow_redirects=True)
        self.assertEqual(returned_value.status_code, 200)

    def test_login(self):
        # Get without a user
        returned_value = self.app_test.get('/login', follow_redirects=True)
        self.assertEqual(returned_value.status_code, 200)
        # POST with a user
        returned_value = self.app_test.post('/login', data=dict(
            username="test",
            password="password"
        ), follow_redirects=True)
        self.assertEqual(returned_value.status_code, 200)
        self.assertTrue(b'Could not log you in!' not in returned_value.data)
        self.assertTrue(b'See Trainers' in returned_value.data)
        self.assertTrue(b'Workouts' in returned_value.data)
        self.assertTrue(b'Schedule' in returned_value.data)

        # POST with a fake user
        returned_value = self.app_test.post('/login', data=dict(
            username="fake",
            password="password"
        ), follow_redirects=True)
        self.assertEqual(returned_value.status_code, 200)
        self.assertTrue(b'Could not log you in!' in returned_value.data)
        self.assertTrue(b'See Trainers' not in returned_value.data)
        self.assertTrue(b'Username' in returned_value.data)
        self.assertTrue(b'Password' in returned_value.data)
        self.assertTrue(b'Login</button>' in returned_value.data)
        self.assertTrue(b'Remember me</label>' in returned_value.data)

    def test_signup(self):
        # Get without a user
        returned_value = self.app_test.get('/signup', follow_redirects=True)
        self.assertEqual(returned_value.status_code, 200)

        # POST with a username that was taken
        returned_value = self.app_test.post('/signup', data=dict(
            username="test",
            password="password",
            repassword="password",
            firstname="first",
            lastname="last",
            location="Earth",
            phone=1234567890
        ), follow_redirects=True)
        print(returned_value.data)
        self.assertEqual(returned_value.status_code, 200)
        self.assertTrue(b'Account was created!' not in returned_value.data)
        self.assertTrue(b'Could not create account' not in returned_value.data)
        self.assertTrue(b'Username was taken' in returned_value.data)
        self.assertTrue(
            b'<form action="/signup" method="POST">' in returned_value.data)

        if self.database.get_by_username("test"):
            self.database.remove_user(
                self.database.get_by_username("test")['_id'])

        # POST with a username that was not taken, success
        returned_value = self.app_test.post('/signup', data=dict(
            username="test",
            password="password",
            repassword="password",
            firstname="first",
            lastname="last",
            location="Earth",
            phone=1234567890
        ), follow_redirects=True)
        print(returned_value.data)
        self.assertEqual(returned_value.status_code, 200)
        self.assertTrue(b'Account was created!' in returned_value.data)
        self.assertTrue(b'Could not create account' not in returned_value.data)
        self.assertTrue(b'Username was taken' not in returned_value.data)
        self.assertTrue(
            b'<form action="/signup" method="POST">' not in returned_value.data)
