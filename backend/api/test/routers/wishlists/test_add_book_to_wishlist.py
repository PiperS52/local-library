import os
import sqlite3
import tempfile
import unittest
from fastapi.testclient import TestClient

from api.app import app
from database.database_service import get_db

class TestAddBookToWishlist(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a temporary SQLite database
        cls.db_fd, cls.db_path = tempfile.mkstemp()
        cls.connection = sqlite3.connect(cls.db_path, check_same_thread=False)
        cls.connection.row_factory = sqlite3.Row
        cursor = cls.connection.cursor()
        # Create tables and seed data
        cursor.execute('''
            CREATE TABLE books (
                id INTEGER PRIMARY KEY,
                isbn TEXT,
                authors TEXT,
                publication_year TEXT,
                title TEXT,
                language TEXT,
                rental_status TEXT,
                rental_date TEXT,
                amazon_url TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE wishlists (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                book_id INTEGER
            )
        ''')
        cursor.execute('''
            INSERT INTO books (id, isbn, authors, publication_year, title, language, rental_status, rental_date, amazon_url)
            VALUES (1, '123', 'Author', '2020', 'Test Book', 'EN', 'available', '2025-06-16', 'https://amazon.com/test-book-1')
        ''')
        cls.connection.commit()

        # Dependency override
        def override_get_db():
            try:
                yield cls.connection
            finally:
                pass  # Don't close here, we'll close in tearDownClass

        app.dependency_overrides[get_db] = override_get_db
        cls.client = TestClient(app)


    @classmethod
    def tearDownClass(cls):
        cls.connection.close()
        os.close(cls.db_fd)
        os.unlink(cls.db_path)

    def test_add_book_to_wishlist_successfully_adds_new_entry_to_wishlists_table(self):
        payload = {"userId": 1, "bookId": 1}
        response = self.client.post("/wishlists", json=payload)
        self.assertEqual(response.status_code, 201)
        # Check DB for updated status
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM wishlists WHERE user_id=1")
        wishlist_entry = cursor.fetchone()
        wishlist_entry_dict = dict(wishlist_entry)
        self.assertEqual(wishlist_entry_dict, {'id': 1, 'user_id': 1, 'book_id': 1})

    def test_add_book_to_wishlist_returns_404_if_book_not_found(self):
        payload = {"userId": 1, "bookId": 101}  # Assuming book with ID 101 does not exist
        response = self.client.post("/wishlists", json=payload)
        self.assertEqual(response.status_code, 404)

    def test_add_book_to_wishlist_returns_400_error_when_invalid_request_body(self):
        payload = {"invalid": "invalid", "bookId": 101}
        response = self.client.post("/wishlists", json=payload)
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()