import os
import sqlite3
import tempfile
import unittest
from fastapi.testclient import TestClient

from api.app import app
from database.database_service import get_db

class TestUpdateBooksAmazonUrls(unittest.TestCase):
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

    def test_update_books_amazon_urls_successfully_updates_relevant_books(self):
        payload = {"books": [{"id": 1, "amazonUrl": "https://amazon.com/updated-test-book-1"}]}
        response = self.client.patch("/books", json=payload)
        self.assertEqual(response.status_code, 204)
        # Check DB for updated status
        cursor = self.connection.cursor()
        cursor.execute("SELECT amazon_url FROM books WHERE id=1")
        updated_book_amazon_url = cursor.fetchone()["amazon_url"]
        self.assertEqual(updated_book_amazon_url, "https://amazon.com/updated-test-book-1")

    def test_update_books_amazon_urls_returns_400_error_when_invalid_request_body(self):
        payload = {"books": [{"invalid": "invalid", "amazonUrl": "https://amazon.com/updated-test-book-1"}]}
        response = self.client.patch("/books", json=payload)
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()