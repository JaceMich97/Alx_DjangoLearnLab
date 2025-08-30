---

### 📄 retrieve.md
markdown
# Retrieve Operation

python
from bookshelf.models import Book

# Get all books
Book.objects.all()

# Get a single book by id
Book.objects.get(id=1)