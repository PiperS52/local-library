import os
import sqlite3
import tempfile
import unittest
from freezegun.api import freeze_time
from fastapi.testclient import TestClient

from api.app import app
from database.database_service import get_db

class TestGetBooksReport(unittest.TestCase):
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
            INSERT INTO books (id, isbn, authors, publication_year, title, language, rental_status, rental_date)
            VALUES (1, '123', 'Author1', '2020', 'Test Book 1', 'EN', 'borrowed', '2025-06-16'), (2, '234', 'Author2', '2022', 'Test Book 2', 'EN', 'borrowed', '2025-06-13')
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

    @freeze_time("2025-06-16")
    def test_get_books_with_no_query_params_returns_all_books(self):
        response = self.client.get("/books-report")
        self.assertEqual(response.status_code, 200)
        books = response.json()
        self.assertEqual(len(books), 2)
        self.assertEqual(books[0]['title'], 'Test Book 1')
        self.assertEqual(books[0]['daysBorrowed'], 0)
        self.assertEqual(books[1]['title'], 'Test Book 2')
        self.assertEqual(books[1]['daysBorrowed'], 3)

if __name__ == "__main__":
    unittest.main()