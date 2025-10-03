from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # books + library
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # authentication
    path('login/',  auth_views.LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),

    # role-protected pages
    path('role/admin/', views.admin_view, name='admin-view'),
    path('role/librarian/', views.librarian_view, name='librarian-view'),
    path('role/member/', views.member_view, name='member-view'),

    # permission-protected book actions
    path('books/add/', views.add_book, name='book-add'),
    path('books/<int:pk>/edit/', views.edit_book, name='book-edit'),
    path('books/<int:pk>/delete/', views.delete_book, name='book-delete'),
]
