from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from .models import Book

@permission_required('bookshelf.can_view', raise_exception=True)
def list_books(request):
    return HttpResponse("can_view OK")

@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    return HttpResponse("can_create OK")

@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    return HttpResponse(f"can_edit OK: {pk}")

@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    return HttpResponse(f"can_delete OK: {pk}")


@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    titles = ", ".join(Book.objects.values_list('title', flat=True))
    return HttpResponse(f"book_list: {titles if titles else 'no books'}")
