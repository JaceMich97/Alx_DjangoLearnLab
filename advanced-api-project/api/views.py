from rest_framework.generics import (
    ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

# ---- NEW: filters for DRF ----
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
# --------------------------------

from .models import Book
from .serializers import BookSerializer


class BookListView(ListAPIView):
    """Public read-only list with filtering, searching, and ordering."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # DRF backends: filter by fields, text-search, and ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Filter by these fields (e.g. ?title=..., ?author=1, ?publication_year=2020)
    filterset_fields = ['title', 'author', 'publication_year']

    # Full-text search on title and related author name (e.g. ?search=asimov)
    search_fields = ['title', 'author__name']

    # Allow ordering by title or publication_year (e.g. ?ordering=title or ?ordering=-publication_year)
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering


class BookDetailView(RetrieveAPIView):
    """Public read-only detail."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(CreateAPIView):
    """Create requires authentication."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookUpdateView(UpdateAPIView):
    """Update requires authentication."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookDeleteView(DestroyAPIView):
    """Delete requires authentication."""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
