from fastapi import APIRouter, Query, HTTPException, Depends
from typing import List
from natsort import natsorted

from models.wishlist import WishlistRequest, WishlistResponse
from database.database_service import get_db


router = APIRouter()

@router.delete(
    "/wishlists/{wishlist_id}",
    summary="Deletes a book wishlist entry",
    status_code=204,
    responses={
        204: {"description": "Wishlist entry deleted successfully"},
        400: {"description": "Invalid parameters"},
        404: {"description": "Book not found"},
    },
    tags=["Wishlists"]
)
def delete_book_from_wishlist(
    wishlist_id: int,
    db=Depends(get_db),
):
    """
    Deletes a wishlist entry.
    :param wishlist_id: the id of the wishlist entry to be deleted
    """

    # check if the wishlist entry exists
    cursor = db.cursor()
    cursor.execute("SELECT * FROM wishlists WHERE id=?", (wishlist_id,))
    existing_wishlist = cursor.fetchone()

    if not existing_wishlist:
        raise HTTPException(status_code=404, detail="Wishlist not found")

    # delete the wishlist entry
    cursor.execute(
        "DELETE FROM wishlists WHERE id=?",
        (wishlist_id,)
    )
    db.commit()