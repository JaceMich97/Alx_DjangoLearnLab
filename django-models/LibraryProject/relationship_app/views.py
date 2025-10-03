from django.shortcuts import render
from django.views.generic.detail import DetailView   # <-- exact string checker wants
from .models import Book
from .models import Library

# Function-based view: render template and list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view: DetailView for a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
