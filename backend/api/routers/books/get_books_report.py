from fastapi import APIRouter, Query, HTTPException, Depends
from typing import List
from natsort import natsorted
from datetime import datetime

from models.book import Book, BookReport
from database.database_service import get_db


router = APIRouter()

@router.get(
    "/books-report",
    summary="Gets a books report showing the books being borrowed and how long they have been borrowed",
    status_code=200,
    responses={
        200: {"model": List[BookReport], "description": "A list of book reports"},
    },
    tags=["Books"]
)
def get_books_report(
    db=Depends(get_db),
):
    """
    Gets a books report showing the books being borrowed and how long they have been borrowed.
    :param db: the database connection
    """

    # fetch all books that are currently borrowed
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books WHERE rental_status='borrowed'")
    books = cursor.fetchall()

    books_dicts = [dict(row) for row in books]

    # calculate the rental duration for each book
    for book in books_dicts:
        if book["rental_date"]:
            rental_duration = (datetime.now() - datetime.strptime(book["rental_date"], "%Y-%m-%d")).days
            book["rental_duration"] = rental_duration
        else:
            book["rental_duration"] = None

    response = [
        {
            "id": book["id"],
            "isbn": book["isbn"],
            "authors": book["authors"],
            "publicationYear": book["publication_year"],
            "title": book["title"],
            "daysBorrowed": book["rental_duration"] if book["rental_duration"] is not None else "N/A"
        } for book in books_dicts
    ]
    
    return natsorted(response, key=lambda x: x['daysBorrowed']) if response else []