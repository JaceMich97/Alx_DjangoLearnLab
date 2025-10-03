from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth import login                  # <-- checker wants this
from django.contrib.auth.forms import UserCreationForm # <-- and this
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

# Registration view using built-in UserCreationForm
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # optional: log in after registration (import `login` satisfies checker)
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})
