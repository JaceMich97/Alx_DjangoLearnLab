from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

# Keeps the simple list endpoint from Task 1
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# Full CRUD endpoint via a ViewSet
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
