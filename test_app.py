import unittest
from app import app


class BookStreakTests(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    # Test 1: Home page works
    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    # Test 2: JSON API works
    def test_books_api(self):
        response = self.client.get("/api/books")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertIn("books", data)

    # Test 3: Health check works
    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)

        data = response.get_json()

        self.assertEqual(data["status"], "ok")


if __name__ == "__main__":
    unittest.main()
