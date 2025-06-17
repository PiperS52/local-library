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
    update_book_rental_status,
    get_books_report,
    update_books_amazon_urls,
)
from routers.wishlists import (
    add_book_to_wishlist,
    delete_book_from_wishlist,
    get_wishlists,
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
app.include_router(update_book_rental_status.router)
app.include_router(get_books_report.router)
app.include_router(update_books_amazon_urls.router)

# Wishlists
app.include_router(add_book_to_wishlist.router)
app.include_router(delete_book_from_wishlist.router)
app.include_router(get_wishlists.router)

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

def seed_wishlists_table(db):
    cursor = db.cursor()
    cursor.execute('SELECT COUNT(*) FROM wishlists')
    count = cursor.fetchone()[0]
    if count == 0:
        try:
            cursor.execute(
                "INSERT INTO wishlists (id, user_id, book_id) VALUES (1, 1, 2), (2, 1, 5), (3, 1, 6), (4, 1, 960), (5, 1, 34), (6, 1, 890), (7, 1, 1934)"
            )
            db.commit()
        except sqlite3.IntegrityError as e:
            print("Some wishlist entries already exist, skipping insertion.", e)
        for row in cursor.execute('SELECT * FROM wishlists'):
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
        seed_wishlists_table(app.state.db)

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