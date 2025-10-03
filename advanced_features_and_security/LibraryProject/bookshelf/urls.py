from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('form-example/', views.form_example, name='form_example'),
]
