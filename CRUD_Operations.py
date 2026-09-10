from sqlalchemy.orm import Session
from sqlalchemy import select
from library_management_system import Author, Book, Member, Borrowing
from datetime import date
from datetime import timedelta

# Table Creation and Relationships
def add_author(session, name, bio=None):
    """Create a new author and save it to the database."""
    new_author = Author(name=name, bio=bio)
    session.add(new_author)
    session.commit()
    session.refresh(new_author)  # Populates the auto-generated id
    return new_author

def add_member(session, name, email, membership_date=None):
    """Create a new member and save it to the database."""
    if membership_date is None:
        membership_date = date.today()
    new_member = Member(name=name, email=email, membership_date=membership_date )
    session.add(new_member)
    session.commit()
    session.refresh(new_member)  # Populates the auto-generated id
    return new_member

def add_book(session, title, isbn, year_published, available_copies, author_names):
    existing = session.execute(
        select(Book).where(Book.isbn==isbn)
    ).scalar_one_or_none()

    if existing:
        raise ValueError(f"A book with this ISBN {isbn} already exists!")

    authors = []
    for name in author_names:
        existing_author = session.execute(
        select(Author).where(Author.name==name)
        ).scalar_one_or_none()
        if existing_author:
            authors.append(existing_author)
        else:
            authors.append(Author(name=name))

    new_book = Book(
        title = title,
        isbn = isbn,
        year_published = year_published,
        available_copies = available_copies,
        authors = authors,
    )
    session.add(new_book)
    session.commit()    
    session.refresh(new_book)
    return new_book

def checkout_book(session, book_id, member_id, checkout_date=None):
    book = session.get(Book, book_id)
    member = session.get(Member, member_id)
    
    if book is None:
        raise ValueError(f"No book with id {book_id}.") # A guard check 
    if member is None:
        raise ValueError(f"No member with id {member_id}.") # A guard check 

    if book.available_copies < 1:
        raise ValueError(f"No available copies of {book.title!r} to check out.")  # A guard check 

    if checkout_date is None:
        checkout_date = date.today()  # Default check out date to whatever date it is when book is checkedout

    new_borrowing = Borrowing(
        book_id=book_id,
        member_id=member_id,
        checkout_date=checkout_date
    )
    book.available_copies -= 1

    session.add(new_borrowing)
    session.commit()
    session.refresh(new_borrowing)
    return new_borrowing

def list_all_books(session):
    result = session.execute(select(Book))
    return result.scalars().all()

def search_books_by_title(session, keyword):
    pattern = f"%{keyword}%"
    result = session.execute(select(Book).where(Book.title.ilike(pattern)))
    return result.scalars().all()

def find_books_by_author(session, author_name):
    pattern = f"%{author_name}%"
    result = session.execute(select(Book).join(Book.authors).where(Author.name.ilike(pattern)))
    return result.scalars().unique().all()

def list_member_borrowings(session, member_id, current_only=True):
    stmt = select(Borrowing).where(Borrowing.member_id == member_id)
    if current_only:
        stmt = stmt.where(Borrowing.return_date.is_(None))

    result = session.execute(stmt)
    return result.scalars().all()


def list_overdue_books(session, loan_period_days=14):
    cut_off_date = date.today() - timedelta(days=loan_period_days)
    stmt = select(Borrowing).where(
        Borrowing.return_date.is_(None),  
        Borrowing.checkout_date <= cut_off_date
    )
    result = session.execute(stmt)
    return result.scalars().all()

