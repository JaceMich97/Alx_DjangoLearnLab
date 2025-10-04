"""
Models for the advanced-api-project.

We model a one-to-many relationship:
- Author has many Book instances.
- Book belongs to a single Author (ForeignKey).
"""
from django.db import models

class Author(models.Model):
    """Author of one or more books."""
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    """A single book written by an Author."""
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    # related_name="books" gives reverse access: author.books.all()
    author = models.ForeignKey(Author, related_name="books", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.title} ({self.publication_year})"
