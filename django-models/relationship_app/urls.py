from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    list_books, LibraryDetailView, RegisterView,
    admin_view, librarian_view, member_view,
    add_book, edit_book, delete_book
)

urlpatterns = [
    # Task 1: function/class views
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Task 2: auth
    path('login/',  LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),

    # Task 3: roles
    path('role/admin/', admin_view, name='admin-view'),
    path('role/librarian/', librarian_view, name='librarian-view'),
    path('role/member/', member_view, name='member-view'),

    # Task 4: permissions CRUD
    path('books/add/', add_book, name='book-add'),
    path('books/<int:pk>/edit/', edit_book, name='book-edit'),
    path('books/<int:pk>/delete/', delete_book, name='book-delete'),
]
