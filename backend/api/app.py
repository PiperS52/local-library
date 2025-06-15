"""
This module contains the main FastAPI app.
"""
import csv
import os

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
import sqlite3

from routers.books import (
    get_books,
)

from database.database_service import get_db, DATABASE

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
BOOKS_CSV = '/app/books.csv'

# Books
app.include_router(get_books.router)

# Wishlists

def seed_books_table(db):
    cursor = db.cursor()
    cursor.execute('SELECT COUNT(*) FROM books')
    count = cursor.fetchone()[0]
    if count == 0 and os.path.exists(BOOKS_CSV):
        with open(BOOKS_CSV, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            books = [(row['Id'], row['ISBN'], row['Authors'], row.get('Publication Year'), row['Title'], row['Language']) for row in reader]
            cursor.executemany(
                'INSERT INTO books (id, isbn, authors, publication_year, title, language) VALUES (?, ?, ?, ?, ?, ?)',
                books
            )
            db.commit()
    for row in cursor.execute('SELECT * FROM books'):
        print(row)

@app.on_event("startup")
async def startup():
    app.state.db = sqlite3.connect(DATABASE, check_same_thread=False)
    app.state.db.row_factory = sqlite3.Row
    # Create tables if they do not exist
    with app.state.db:
        app.state.db.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isbn TEXT UNIQUE,
                authors TEXT NOT NULL,
                publication_year TEXT NOT NULL,
                title TEXT NOT NULL,
                language TEXT NOT NULL,
                rental_status TEXT,
                rental_date TEXT,
                amazon_url TEXT
            )
        ''')
        app.state.db.execute('''
            CREATE TABLE IF NOT EXISTS wishlists (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                FOREIGN KEY (book_id) REFERENCES books (id)
            )
        ''')
        # Seed data if needed
        seed_books_table(app.state.db)

@app.on_event("shutdown")
async def shutdown():
    if hasattr(app.state, 'db'):
        app.state.db.close()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_, exc):
    """
    Transforms the default FastAPI validation error response into a 400.
    """
    return PlainTextResponse(str(exc), status_code=400)