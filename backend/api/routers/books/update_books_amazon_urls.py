from fastapi import APIRouter, Query, HTTPException, Depends
from typing import List
from natsort import natsorted

from models.book import UpdateBookAmazonUrlRequest
from database.database_service import get_db


router = APIRouter()

@router.patch(
    "/books",
    summary="Updates the amazon url book",
    status_code=204,
    responses={
        204: {"description": "Books amazon urls updated successfully"},
        400: {"description": "Invalid parameters"}
    },
    tags=["Books"]
)
def update_books_amazon_urls(
    updated_books: UpdateBookAmazonUrlRequest,
    db=Depends(get_db),
):
    """
    Updates the books amazon url.
    :param updated_books: the updated amazon url details of the books
    """

    # fetch each book and update its amazon url
    cursor = db.cursor()
    for book in updated_books.books:
        cursor.execute("SELECT * FROM books WHERE id=?", (book.id,))
        existing_book = cursor.fetchone()
        if not existing_book:
            raise HTTPException(status_code=404, detail=f"Book with id {book.id} not found")

        cursor.execute(
            "UPDATE books SET amazon_url = ? WHERE id = ?",
            (book.amazon_url, book.id)
        )
    db.commit()
