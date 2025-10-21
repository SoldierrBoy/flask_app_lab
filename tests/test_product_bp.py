import unittest
from app import app

class ProductsBlueprintTestCase(unittest.TestCase):

    def setUp(self):

        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_products_list_page(self):

        response = self.client.get("/products/")
        # Перевіряємо, що сторінка відкрилась
        self.assertEqual(response.status_code, 200)
        # Перевіряємо, що на сторінці є правильний текст
        self.assertIn(b"This is the list of products.", response.data)

    def test_product_details_page(self):

        response = self.client.get("/products/123")
        # Перевіряємо, що сторінка відкрилась
        self.assertEqual(response.status_code, 200)
        # Перевіряємо, що ID товару відображається на сторінці
        self.assertIn(b"Product ID: 123", response.data)