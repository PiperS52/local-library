from fastapi import APIRouter, Query, HTTPException, Depends
from typing import List
from natsort import natsorted

from models.book import UpdateBookRentalStatusRequest
from database.database_service import get_db


router = APIRouter()

@router.patch(
    "/books/{book_id}/rental-status",
    summary="Updates the rental status of a book",
    status_code=204,
    responses={
        204: {"description": "Book rental status updated successfully"},
        400: {"description": "Invalid parameters"}
    },
    tags=["Books"]
)
def update_book_rental_status(
    book_id: int,
    updated_book: UpdateBookRentalStatusRequest,
    db=Depends(get_db),
):
    """
    Updates a book rental status.
    :param book_id: the id of the book
    :param updated_book: the updated rental status details of the book
    """

    # check if the book exists
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books WHERE id=?", (book_id,))
    book = cursor.fetchone()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # update the book rental status
    cursor.execute(
        "UPDATE books SET rental_status = ? WHERE id = ?",
        (updated_book.rental_status, book_id)
    )
    db.commit()

    if updated_book.rental_status == "borrowed":
        cursor.execute(
            "UPDATE books SET rental_date = date('now') WHERE id = ?",
            (book_id,)
        )
        db.commit()
    elif updated_book.rental_status == "available":
        cursor.execute(
            "UPDATE books SET rental_date = NULL WHERE id = ?",
            (book_id,)
        )
        db.commit()
        cursor.execute("SELECT user_id FROM wishlists WHERE book_id=?", (book_id,))
        wishlist_entries = cursor.fetchall()
        wishlist_entry_dicts = [dict(row) for row in wishlist_entries]
        if wishlist_entry_dicts:
            book_name = dict(book)['title']
            for entry in wishlist_entry_dicts:
                # Notify users who have this book in their wishlist
                send_email_notification(entry['user_id'], book_name)


def send_email_notification(user_id: str, book_name: str):
    # Placeholder for email notification logic
    print(f"Notifying user {user_id} that the book {book_name} is now availabile.")
    pass