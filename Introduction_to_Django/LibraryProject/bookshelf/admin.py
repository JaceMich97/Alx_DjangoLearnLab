from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "publication_date", "isbn", "pages", "cover", "language")
    search_fields = ("title", "author", "isbn")
    list_filter = ("author", "publication_date", "language")