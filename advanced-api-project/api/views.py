"""
Generic API views for Book.

We provide:
- BookList   (ListAPIView):    GET /api/books/
- BookDetail (RetrieveAPIView):GET /api/books/<pk>/
- BookCreate (CreateAPIView):  POST /api/books/create/
- BookUpdate (UpdateAPIView):  PUT/PATCH /api/books/<pk>/update/
- BookDelete (DestroyAPIView): DELETE /api/books/<pk>/delete/

Permissions:
- Read-only endpoints (list/detail): AllowAny
- Mutating endpoints (create/update/delete): IsAuthenticated
"""
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class BookDetail(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class BookCreate(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookUpdate(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

class BookDelete(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
