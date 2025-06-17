from fastapi_camelcase import CamelModel
from typing import List


class Book(CamelModel):
    """
    Represents a book returned in a response.
    """

    id: int
    isbn: str
    authors: str
    publication_year: str
    title: str
    rental_status: str = "available"  # Default value for rental status


class UpdateBookRentalStatusRequest(CamelModel):
    """
    Represents an update book rental status request.
    """
    # TODO: change to enum
    rental_status: str


class BookReport(Book, CamelModel):
    """
    Represents a book report.
    """
    rental_date: str
    days_borrowed: int


class UpdateBookAmazonUrlItem(CamelModel):
    """
    Represents an update book amazon url item.
    """
    id: int
    amazon_url: str

class UpdateBookAmazonUrlRequest(CamelModel):
    """
    Represents an update book amazon url request.
    """
    books: List[UpdateBookAmazonUrlItem]