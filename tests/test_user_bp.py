import unittest
from app import create_app, db

class UserBlueprintTests(unittest.TestCase):

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

    def test_greetings_route_works(self):

        response = self.client.get("/users/hi/Maria?age=25")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"MARIA", response.data)
        self.assertIn(b"25", response.data)

    def test_admin_redirect_shows_correct_content(self):

        response = self.client.get("/users/admin", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ADMINISTRATOR", response.data)
        self.assertIn(b"age is unknown", response.data)