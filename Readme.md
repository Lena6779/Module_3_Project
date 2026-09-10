# 📚 Library Management System

A command-line library system built with **SQLAlchemy 2.0** (`Mapped` /
`mapped_column` style ORM models) and **SQLite**.

## Setup

```bash
pip install sqlalchemy
python main.py
```

Running `main.py` will:
1. Create `library_management_system.db` and all tables from the ORM
   models (no raw SQL anywhere).
2. Drop you into the interactive menu.

To load sample data first, run:

```bash
python seed.py
```

This populates the database with 5 books, 5 authors, 4 members, and 6
borrowings (4 returned, 2 still outstanding) so the system is easy to
demo right away. It's safe to run more than once — it checks for
existing data and skips reseeding if the database isn't empty.

## Files

| File                          | Purpose                                                        |
|--------------------------------|------------------------------------------------------------------|
| `library_management_system.py` | SQLAlchemy 2.0 models: `Member`, `Author`, `Book`, `Borrowing`, plus the `book_authors` many-to-many association table, and the database engine |
| `crud.py`                      | All Create/Read/Update/Delete functions                        |
| `seed.py`                      | Populates sample data for demoing                               |
| `main.py`                      | The interactive CLI menu                                       |

## Data model

- **members** `(id, name, email UNIQUE, membership_date)`
- **authors** `(id, name, bio)`
- **books** `(id, title, isbn UNIQUE, year_published, available_copies)`
- **book_authors** — pure association table for the books ↔ authors
  many-to-many relationship (a book can have several authors, e.g.
  *Good Omens* by Pratchett & Gaiman; an author can have several books,
  e.g. Tolkien wrote both *The Hobbit* and *The Fellowship of the Ring*).
- **borrowings** `(id, book_id, member_id, checkout_date, return_date)` —
  the books ↔ members relationship, modeled as its own table (rather than
  a plain association table) since it carries extra data. `return_date`
  is `NULL` while the book is still checked out. A borrowing counts as
  **overdue** once `checkout_date` is more than 14 days in the past and
  `return_date` is still `NULL`.

## CRUD coverage

- **Create:** `add_book`, `add_member`, `add_author`, `checkout_book`
- **Read:** `list_all_books`, `search_books_by_title`, `find_books_by_author`,
  `list_member_borrowings`, `list_overdue_books`
- **Update:** `return_book` (sets `return_date`, restocks the copy),
  `update_member_email`
- **Delete:** `remove_book` (blocked if the book has an active/unreturned
  borrowing), `remove_member` (blocked if the member has active
  borrowings)

## CLI menu

```
📚 Library Management System
1. Add a book
2. Add a member
3. Search books
4. Check out a book
5. Return a book
6. View member's borrowings
7. View overdue books
8. Exit
```

The menu loops until you choose 8. Each option prompts for whatever it
needs and prints a clear confirmation or a friendly error message
(duplicate ISBN, duplicate email, no copies available, book/member not
found, etc.) instead of crashing.

## Design notes

- SQLite via a local `.db` file for zero-setup local demoing.
- `add_book` looks up authors by exact name and reuses existing `Author`
  rows instead of creating duplicates, so a second book by a known
  author links to the same author record rather than creating a
  duplicate.
- `checkout_book` / `return_book` keep `available_copies` in sync:
  checking out decrements it, returning increments it back, and
  checking out is blocked once a book has zero copies available.
- Deleting a book or member is blocked while there's an active
  (unreturned) borrowing, per the assignment's delete rules.
- Every Create/Update/Delete function raises a clear `ValueError` on
  invalid input (not found, duplicate, no copies, already returned,
  etc.), which the CLI catches and displays instead of crashing.