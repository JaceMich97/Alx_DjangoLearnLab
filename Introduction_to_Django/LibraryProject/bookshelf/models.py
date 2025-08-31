from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13)
    pages = models.IntegerField()
    cover = models.CharField(max_length=100, default="Unknown")  # added default
    language = models.CharField(max_length=50, default="English")  # safe default

    def __str__(self):
        return self.title