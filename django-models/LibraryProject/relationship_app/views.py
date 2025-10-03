from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library

# --- Function-based view: simple text list of "title by author" ---
def list_books(request):
    lines = [f"{b.title} by {b.author.name}" for b in Book.objects.select_related('author').all()]
    body = "\n".join(lines) if lines else "No books yet."
    return HttpResponse(body, content_type="text/plain")

# --- Class-based view: DetailView for a specific library ---
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
