from fastapi import APIRouter, Query, HTTPException, Depends
from typing import List
from natsort import natsorted

from models.wishlist import WishlistRequest, WishlistResponse
from database.database_service import get_db


router = APIRouter()

@router.post(
    "/wishlists",
    summary="Creates a book wishlist entry",
    status_code=201,
    responses={
        201: {"model": WishlistResponse, "description": "A newly created wishlist entry"},
        400: {"description": "Invalid parameters"},
        404: {"description": "Book not found"},
    },
    tags=["Wishlists"]
)
def add_book_to_wishlist(
    new_wishlist: WishlistRequest,
    db=Depends(get_db),
):
    """
    Creates a new wishlist entry.
    :param new_wishlist: the details of the wishlist entry to be created
    """

    # check if the book exists
    cursor = db.cursor()
    cursor.execute("SELECT * FROM books WHERE id=?", (new_wishlist.book_id,))
    book = cursor.fetchone()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # check if the user already has this book in their wishlist
    cursor.execute("SELECT * FROM wishlists WHERE user_id=? AND book_id=?", (new_wishlist.user_id, new_wishlist.book_id))
    existing_wishlist = cursor.fetchone()

    if existing_wishlist:
        raise HTTPException(status_code=400, detail="Book already in wishlist")
    # insert the new wishlist entry
    cursor.execute(
        "INSERT INTO wishlists (user_id, book_id) VALUES (?, ?)",
        (new_wishlist.user_id, new_wishlist.book_id)
    )
    db.commit()
    new_wishlist_id = cursor.lastrowid

    return {
        "id": new_wishlist_id,
        "userId": new_wishlist.user_id,
        "bookId": new_wishlist.book_id
    }