from .models import Author, Book, Library, Librarian

def books_by_author(author_name: str):
    """Query all books by a specific author (uses reverse relation)."""
    try:
        author = Author.objects.get(name=author_name)
        return author.books.all()
    except Author.DoesNotExist:
        return Book.objects.none()

def books_in_library(library_name: str):
    """List all books in a library (uses reverse M2M relation)."""
    try:
        library = Library.objects.get(name=library_name)
        return library.books.all()
    except Library.DoesNotExist:
        return Book.objects.none()

def librarian_for_library(library_name: str):
    """Retrieve the librarian for a library (OneToOne reverse accessor)."""
    try:
        library = Library.objects.get(name=library_name)
        return library.librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None
