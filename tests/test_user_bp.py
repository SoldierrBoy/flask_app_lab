import unittest
from app import app


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        """Налаштування, яке виконується перед кожним тестом."""
        # Вмикаємо режим тестування. Це вимикає, наприклад, сторінки з помилками.
        app.config['TESTING'] = True
        # Створюємо тестовий клієнт, який буде "вдавати" з себе браузер
        self.client = app.test_client()

    def test_greetings_page(self):
        """Тест для маршруту /users/hi/<name>."""
        # Робимо GET-запит на сторінку, як це робив би браузер
        # ВАЖЛИВО: ми додали префікс /users, який налаштували раніше
        response = self.client.get("/users/hi/John?age=30")

        # Перевіряємо, чи сторінка повернула статус 200 (ОК)
        self.assertEqual(response.status_code, 200)
        # Перевіряємо, чи на сторінці є очікуваний текст (у байтах)
        self.assertIn(b"JOHN", response.data)
        self.assertIn(b"30", response.data)

    def test_admin_page_redirect(self):
        """Тест для маршруту /users/admin, який перенаправляє."""
        # Робимо запит, автоматично слідуючи за перенаправленням (redirect)
        response = self.client.get("/users/admin", follow_redirects=True)

        # Перевіряємо, що фінальна сторінка відкрилась успішно
        self.assertEqual(response.status_code, 200)
        # Перевіряємо, що на фінальній сторінці є очікуваний текст
        self.assertIn(b"ADMINISTRATOR", response.data)


if __name__ == '__main__':
    unittest.main()