# Create Operation

```python
from bookshelf.models import Book

# Create a new Book object
book = Book.objects.create(
    title="Django Basics",
    author="Udoka",
    published_year=2025
)