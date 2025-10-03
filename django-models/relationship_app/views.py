from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.http import HttpResponse
from django import forms
from .models import Book, Library

# --- Task 1: function-based view (PLAIN TEXT) ---
def list_books(request):
    """
    Returns a simple text list: "<title> by <author>"
    One per line (text/plain), as the checker expects.
    """
    lines = [f"{b.title} by {b.author.name}" for b in Book.objects.select_related('author').all()]
    body = "\n".join(lines) if lines else "No books yet."
    return HttpResponse(body, content_type="text/plain")

# --- Task 1: class-based view for a specific library ---
class LibraryDetailView(DetailView):
    """
    Displays details for a specific Library and lists its books.
    Uses DetailView as required.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

# --- Task 2: registration (login/logout use built-ins in urls) ---
class RegisterView(View):
    template_name = 'relationship_app/register.html'
    def get(self, request):
        return render(request, self.template_name, {'form': UserCreationForm()})
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, self.template_name, {'form': form})

# --- Task 3: role-based views ---
def is_admin(user): return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'
def is_librarian(user): return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'
def is_member(user): return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@user_passes_test(is_admin)
def admin_view(request): return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request): return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request): return render(request, 'relationship_app/member_view.html')

# --- Task 4: permission-protected CRUD on Book ---
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author']

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/book_form.html', {'form': form, 'action': 'Add'})

@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/book_form.html', {'form': form, 'action': 'Edit'})

@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/book_confirm_delete.html', {'book': book})
