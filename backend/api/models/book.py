from fastapi_camelcase import CamelModel


class Book(CamelModel):
    """
    Represents a book returned in a response.
    """

    id: float
    isbn: str
    authors: str
    publication_year: str
    title: str
    rental_status: str = "available"  # Default value for rental status