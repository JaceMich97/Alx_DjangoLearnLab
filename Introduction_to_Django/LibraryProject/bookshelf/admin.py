from django.contrib import admin
from .models import Book

class BookAdmin(admin.ModelAdmin):
    # Show these fields as columns in the list view
    list_display = ('title', 'author', 'publication_date')

    # Add filters on the right-hand side
    list_filter = ('author', 'publication_date')

    # Add a search bar at the top
    search_fields = ('title', 'author')

# Register the Book model with this custom admin class
admin.site.register(Book, BookAdmin)