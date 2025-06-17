import os
import sqlite3
import tempfile
import unittest
from fastapi.testclient import TestClient

from api.app import app  # Adjust if your FastAPI app is elsewhere
from database.database_service import get_db

class TestUpdateBookRentalStatus(unittest.TestCase):
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
            INSERT INTO books (id, isbn, authors, publication_year, title, language, rental_status)
            VALUES (1, '123', 'Author', '2020', 'Test Book', 'EN', 'available')
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

    def test_update_book_rental_status(self):
        payload = {"rentalStatus": "borrowed"}
        response = self.client.patch("/books/1/rental-status", json=payload)
        print('line 65', response.status_code, response.text) 
        self.assertEqual(response.status_code, 204)
        # Check DB for updated status
        cursor = self.connection.cursor()
        cursor.execute("SELECT rental_status FROM books WHERE id=1")
        status = cursor.fetchone()["rental_status"]
        self.assertEqual(status, "borrowed")

    def test_update_nonexistent_book(self):
        payload = {"rentalStatus": "borrowed"}
        response = self.client.patch("/books/999/rental-status", json=payload)
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()