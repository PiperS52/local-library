from fastapi_camelcase import CamelModel


class WishlistRequest(CamelModel):
    """
    Represents a wishlist request.
    """

    user_id: int
    book_id: int

class WishlistResponse(CamelModel):
    """
    Represents a wishlist returned in a response.
    """

    id: int
    user_id: int
    book_id: int