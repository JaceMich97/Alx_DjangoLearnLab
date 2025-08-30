# Get the book
book = Book.objects.get(id=1)

# Delete it
book.delete()

# Confirm deletion
Book.objects.all()