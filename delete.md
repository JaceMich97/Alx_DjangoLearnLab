---

### 📄 delete.md
markdown
# Delete Operation

python
from bookshelf.models import Book

# Delete a book
book = Book.objects.get(id=1)
book.delete()