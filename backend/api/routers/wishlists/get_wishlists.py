from fastapi import APIRouter, Query, HTTPException, Depends
from typing import List
from natsort import natsorted

from models.book import Book
from database.database_service import get_db


router = APIRouter()

@router.get(
    "/wishlists",
    summary="Gets a users wishlists querying user_id",
    status_code=200,
    responses={
        200: {"model": List[Book], "description": "A list of books"},
        400: {"description": "Invalid parameters"}
    },
    tags=["Books"]
)
def get_wishlists(
    user_id: str = Query("", alias="userId"),
    db=Depends(get_db),
):
    """
    Gets a users wishlists querying user_id
    :param user_id: the id of the user
    """
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required")

    cursor = db.cursor()
    cursor.execute("SELECT * FROM books INNER JOIN wishlists ON books.id = wishlists.book_id WHERE wishlists.user_id=?", (user_id,))
   
    books = cursor.fetchall()

    books_dicts = [dict(row) for row in books]

    response = [
        {
            "id": book["id"],
            "isbn": book["isbn"],
            "authors": book["authors"],
            "publicationYear": book["publication_year"],
            "title": book["title"],
            "rentalStatus": book["rental_status"] if book["rental_status"] is not None else "available"
        } for book in books_dicts
    ]
    
    return natsorted(response, key=lambda x: x['title']) if response else []