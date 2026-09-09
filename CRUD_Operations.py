from sqlalchemy import select
from sqlalchemy.orm import Session
from library_management_system import Author, Book, Member, Borrowing

def add_author(session, name, bio=None):
    """Create a new author and save it to the database."""
    new_author = Author(name=name, bio=bio)
    session.add(new_author)
    session.commit()
    session.refresh(new_author)  # Populates the auto-generated id
    return new_author

def add_member(session, name, bio=None):
    """Create a new author and save it to the database."""
    new_author = Author(name=name, bio=bio)
    session.add(new_author)
    session.commit()
    session.refresh(new_author)  # Populates the auto-generated id
    return new_author
