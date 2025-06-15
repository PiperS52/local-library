"""
Module for the GET fee calculation endpoint
"""
from fastapi import APIRouter, Query, HTTPException, Depends
from typing import List
from natsort import natsorted

from models.book import Book
from database.database_service import get_db


router = APIRouter()

@router.get(
    "/books",
    summary="Gets books, optionally querying by title and author",
    status_code=200,
    responses={
        200: {"model": List[Book], "description": "A list of books"},
        400: {"description": "Invalid parameters"}
    },
    tags=["Books"]
)
def get_books(
    title: str = Query("", alias="title"),
    author: str = Query("", alias="author"),
    db=Depends(get_db),
):
    """
    Gets books, optionally filtering by title and author.
    :param title: the title of the book
    :param author: the author of the book
    """

    cursor = db.cursor()
    query = "SELECT * FROM books WHERE 1=1"
    params = []
    if title:
        query += " AND title LIKE ?"
        params.append(f"%{title}%")
    if author:
        query += " AND authors LIKE ?"
        params.append(f"%{author}%")
    cursor.execute(query, params)
    books = cursor.fetchall()

    books_dicts = [dict(row) for row in books]

    response = [
        {
            "id": book["id"],
            "isbn": book["isbn"],
            "authors": book["authors"],
            "publicationYear": book["publication_year"],
            "title": book["title"]
        } for book in books_dicts
    ]
    
    return natsorted(response, key=lambda x: x['title']) if response else []