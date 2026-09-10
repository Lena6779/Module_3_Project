from library_management_system import engine, Base
from sqlalchemy.orm import Session
import crud

Base.metadata.create_all(engine)


MENU = """
📚 Library Management System
1. Add a book
2. Add a member
3. Search books
4. Check out a book
5. Return a book
6. View member's borrowings
7. View overdue books
8. Exit
"""

def main():
    with Session(engine) as session:
        while True:
            print(MENU)
            choice = input("Choose an option: ")

            if choice == "8":
                print("Goodbye!")
                break
            elif choice == "1":
                title = input("Title: ")
                isbn = input("ISBN: ")
                year_published = int(input("Year published: "))
                available_copies = int(input("Number of copies: "))
                author_names_raw = input("Author name(s), comma-separated: ")
                author_names = author_names_raw.split(",")

                try:
                    new_book = crud.add_book(session, title, isbn, year_published, available_copies, author_names)
                    print(f"Added: {new_book.title} (id={new_book.id})")
                except ValueError as e:
                    print(f"Error: {e}")

            elif choice == "2":
                name = input("Name: ")
                email = input("Email: ")
                try:
                    new_member = crud.add_member(session, name, email)
                    print(f"Added: {new_member.name} (id={new_member.id})")
                except ValueError as e:
                    print(f"Error: {e}")

            elif choice == "3":
                print("1. Search by title")
                print("2. Search by author")
                search_choice = input("Choose: ")   
                if search_choice == "1":
                    keyword = input("Title contains: ")
                    results = crud.search_books_by_title(session, keyword)
                elif search_choice == "2":
                    keyword = input("Author name contains: ")
                    results = crud.find_books_by_author(session, keyword)
                else:
                    print("Not a valid choice.")
                    results = []

                if not results:
                    print("No matching books found.")
                else:
                    for book in results:
                        authors = ", ".join(a.name for a in book.authors)
                        print(f"  [{book.id}] {book.title!r} by {authors} ({book.available_copies} available)")            

            elif choice == "4":
                book_id = int(input("Book id: "))
                member_id = int(input("Member id: "))
                try:
                    borrowing = crud.checkout_book(session, book_id, member_id)
                    print(f"Checked out. Borrowing id {borrowing.id}.")
                except ValueError as e:
                    print(f"Error: {e}")

            elif choice == "5":
                borrowing_id = int(input("Borrowing id: "))
                try:
                    returned = crud.return_book(session, borrowing_id)
                    print(f"Returned: {returned.book.title!r} on {returned.return_date}.")
                except ValueError as e:
                    print(f"Error: {e}")

            elif choice == "6":
                member_id = int(input("Member id: "))
                borrowings = crud.list_member_borrowings(session, member_id)

                if not borrowings:
                    print("No current borrowings.")
                else:
                    for b in borrowings:
                        print(f"[{b.id}] {b.book.title!r} checked out {b.checkout_date}")

            elif choice == "7":
                overdue = crud.list_overdue_books(session)
                if not overdue:
                    print("Nothing is overdue.")
                else:
                    for b in overdue:
                     print(f"  [{b.id}] {b.book.title!r} borrowed by {b.member.name} "
                    f"(checked out {b.checkout_date})")

                    









if __name__ == "__main__":
    main()