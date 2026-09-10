from datetime import date, timedelta
from library_management_system import engine
from sqlalchemy.orm import Session
import crud


def seed_data():
    with Session(engine) as session:
        existing_books = crud.list_all_books(session)
        if existing_books:
            print("Database already has data -- skipping seed.")
            return

        # Add book data
        b1 = crud.add_book(session, "The Hobbit", "978-0-618-00221-3", 1937, 3, ["J.R.R. Tolkien"])
        b2 = crud.add_book(session, "The Fellowship of the Ring", "978-0-618-00222-0", 1954, 2, ["J.R.R. Tolkien"])
        b3 = crud.add_book(session, "A Short History of Nearly Everything", "978-0-7679-0818-4", 2003, 2, ["Bill Bryson"])
        b4 = crud.add_book(session, "Sapiens", "978-0-06-231609-7", 2011, 1, ["Yuval Noah Harari"])
        b5 = crud.add_book(session, "Good Omens", "978-0-06-085398-3", 1990, 2, ["Terry Pratchett", "Neil Gaiman"])

        # Add member data
        m1 = crud.add_member(session, "Bo Dennis", "bo.dennis@example.com", date.today() - timedelta(days=400))
        m2 = crud.add_member(session, "Harry Potter", "harry.potter@example.com", date.today() - timedelta(days=200))
        m3 = crud.add_member(session, "Cinder Blackburn", "cinder.blackburn@example.com", date.today() - timedelta(days=90))
        m4 = crud.add_member(session, "Dyson Thornwood", "dyson.thornwood@example.com", date.today() - timedelta(days=15))

        # Add borrowings
        loan1 = crud.checkout_book(session, b1.id, m1.id, checkout_date=date.today() - timedelta(days=20))
        crud.return_book(session, loan1.id, return_date=date.today() - timedelta(days=10))

        loan2 = crud.checkout_book(session, b2.id, m2.id, checkout_date=date.today() - timedelta(days=20))
        crud.return_book(session, loan2.id, return_date=date.today() - timedelta(days=10))

        loan3 = crud.checkout_book(session, b3.id, m3.id, checkout_date=date.today() - timedelta(days=20))
        crud.return_book(session, loan3.id, return_date=date.today() - timedelta(days=10))

        loan4 = crud.checkout_book(session, b5.id, m4.id, checkout_date=date.today() - timedelta(days=20))
        crud.return_book(session, loan4.id, return_date=date.today() - timedelta(days=10))

        loan5 = crud.checkout_book(session, b1.id, m4.id, checkout_date=date.today() - timedelta(days=20))
        
        loan6 = crud.checkout_book(session, b1.id, m1.id, checkout_date=date.today() - timedelta(days=20))

if __name__ == "__main__":
    seed_data()