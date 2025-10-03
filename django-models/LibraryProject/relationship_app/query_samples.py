from .models import Author, Book, Library, Librarian

def books_by_author(author_name: str):
    """Query all books by a specific author name."""
    return Book.objects.select_related('author').filter(author__name=author_name)

def books_in_library(library_name: str):
    """List all books in a library by library name."""
    try:
        lib = Library.objects.get(name=library_name)
        return lib.books.select_related('author').all()
    except Library.DoesNotExist:
        return Book.objects.none()

def librarian_for_library(library_name: str):
    """Retrieve the librarian for a library by library name."""
    try:
        lib = Library.objects.get(name=library_name)
        return lib.librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None
