from sqlalchemy import create_engine, String, Date, ForeignKey, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from typing import Optional, List
from datetime import date
 
# --- Engine: Connects to a SQLite database file ---
engine = create_engine(
    "sqlite:///library_management_system.db",
    echo=True  # Prints the SQL that SQLAlchemy generates (great for learning!)
)

# --- Base Class: All models inherit from this ---
class Base(DeclarativeBase):
    pass


# Association Table for books <--> authors
book_authors = Table(
    "book_authors",
    Base.metadata,
    Column("book_id", ForeignKey("books.id"), primary_key=True),
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
)

class Member(Base):
    __tablename__ = "members"  # The actual table name in the database

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    membership_date: Mapped[date] = mapped_column(Date, nullable=False)
    borrowings: Mapped[List["Borrowing"]] = relationship(back_populates="member")

class Author(Base):
    __tablename__ = "authors"  # The actual table name in the database
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    bio: Mapped[Optional[str]] = mapped_column(String(500))  # Optional — can be NULL
    books: Mapped[List["Book"]] = relationship(secondary=book_authors, back_populates="authors")

class Book(Base):
    __tablename__ = "books"  # The actual table name in the database
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    isbn: Mapped[str] = mapped_column(String(100), unique=True,nullable=False)
    year_published: Mapped[int] = mapped_column(nullable=False)
    available_copies: Mapped[int] = mapped_column(nullable=False, default=1)
    borrowings: Mapped[List["Borrowing"]] = relationship(back_populates="book")
    authors: Mapped[List["Author"]] = relationship(secondary=book_authors, back_populates="books")

class Borrowing(Base):
    __tablename__ = "borrowings"  # The actual table name in the database
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"), nullable=False)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), nullable=False)
    checkout_date: Mapped[date] = mapped_column(Date, nullable=False)
    return_date: Mapped[Optional[date]] = mapped_column(Date)
    book: Mapped["Book"] = relationship(back_populates="borrowings")
    member: Mapped["Member"] = relationship(back_populates="borrowings")
