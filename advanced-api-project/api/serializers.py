"""
Serializers for Author and Book.

- BookSerializer: serializes all fields and validates that
  publication_year is not in the future.
- AuthorSerializer: includes a nested, read-only list of books.
"""
from datetime import date
from rest_framework import serializers
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    """Serialize Book and ensure publication_year is not in the future."""
    class Meta:
        model = Book
        fields = ["id", "title", "publication_year", "author"]

    def validate_publication_year(self, value: int) -> int:
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                "publication_year cannot be in the future."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serialize Author including nested books.
    Uses related_name='books' from the Book model's ForeignKey.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["id", "name", "books"]
