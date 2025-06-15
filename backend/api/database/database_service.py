import sqlite3

DATABASE = '/app/app.db'


def get_db():
    """
    Provides a database connection for each router.
    """
    db = sqlite3.connect(DATABASE, check_same_thread=False)
    db.row_factory = sqlite3.Row
    try:
        yield db
    finally:
        db.close()