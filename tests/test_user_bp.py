import unittest
from app import create_app, db
from app.users.models import User


class UserAuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_registration_process(self):
        response = self.client.post('/users/register', data={
            'username': 'new_student',
            'email': 'student@test.com',
            'password': 'secure_password',
            'confirm_password': 'secure_password'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account created successfully', response.data)

        user = db.session.scalar(db.select(User).where(User.username == 'new_student'))
        self.assertIsNotNone(user)

    def test_login_and_logout_flow(self):

        self.client.post('/users/register', data={
            'username': 'auth_user',
            'email': 'auth@test.com',
            'password': 'my_password',
            'confirm_password': 'my_password'
        }, follow_redirects=True)


        response = self.client.post('/users/login', data={
            'username': 'auth_user',
            'password': 'my_password'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back, auth_user!', response.data)
        self.assertIn(b'auth_user', response.data)

        response = self.client.post('/users/logout', follow_redirects=True)
        self.assertIn(b'You have been logged out.', response.data)
        self.assertIn(b'Login', response.data)

    def test_protected_page_access(self):
        response = self.client.get('/users/profile', follow_redirects=True)
        self.assertIn(b'Please log in to access this page.', response.data)