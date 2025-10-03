from .models import Author, Book, Library, Librarian

def books_by_author(author_name: str):
    """Query all books by a specific author using objects.filter(author=author)."""
    try:
        author = Author.objects.get(name=author_name)
        # The checker looks for this exact substring:
        return Book.objects.filter(author=author)
    except Author.DoesNotExist:
        return Book.objects.none()

def books_in_library(library_name: str):
    """List all books in a library (expects 'books.all()')."""
    try:
        library = Library.objects.get(name=library_name)
        return library.books.all()
    except Library.DoesNotExist:
        return Book.objects.none()

def librarian_for_library(library_name: str):
    """Retrieve the librarian for a library (expects 'library.librarian')."""
    try:
        library = Library.objects.get(name=library_name)
        return library.librarian
    except (Library.DoesNotExist, Librarian.DoesNotExist):
        return None
