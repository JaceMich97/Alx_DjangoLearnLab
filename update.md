---

### 📄 update.md
markdown
# Update Operation

python
from bookshelf.models import Book

# Update a book
book = Book.objects.get(id=1)
book.title = "Advanced Django"
book.save()