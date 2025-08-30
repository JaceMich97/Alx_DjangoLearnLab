# Get the book first
book = Book.objects.get(id=1)

# Update its fields
book.title = "No Longer at Ease"
book.publication_year = 1960
book.save()
book