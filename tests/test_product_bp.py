import unittest
from app import create_app, db

class ProductBlueprintTests(unittest.TestCase):

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

    def test_products_list_page_loads(self):

        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"list of products", response.data)

    def test_product_details_page_shows_id(self):

        response = self.client.get("/products/777")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Product ID: 777", response.data)