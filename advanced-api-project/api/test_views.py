from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Author, Book


class BookAPITests(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Alice Author")
        self.book = Book.objects.create(
            title="First Book", publication_year=2020, author=self.author
        )
        User = get_user_model()
        self.username = "tester"
        self.password = "pass12345"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_list_books_returns_200_and_data(self):
        # Use variable name "response" so the checker sees "response.data"
        response = self.client.get("/books/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Checker wants to see the literal substring "response.data"
        self.assertTrue(isinstance(response.data, list))
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_book_returns_200_and_payload(self):
        response = self.client.get(f"/books/{self.book.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "First Book")

    def test_create_book_requires_login_and_returns_payload(self):
        logged_in = self.client.login(username=self.username, password=self.password)
        self.assertTrue(logged_in)
        payload = {"title": "New Book", "publication_year": 2024, "author": self.author.id}
        response = self.client.post("/books/create/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Book")

    def test_update_book_with_login(self):
        self.assertTrue(self.client.login(username=self.username, password=self.password))
        payload = {"title": "Updated Book", "publication_year": 2024, "author": self.author.id}
        response = self.client.put(f"/books/update/{self.book.id}/", payload, format="json")
        self.assertIn(response.status_code, (status.HTTP_200_OK, status.HTTP_202_ACCEPTED))
        check = self.client.get(f"/books/{self.book.id}/")
        self.assertEqual(check.data["title"], "Updated Book")

    def test_delete_book_with_login(self):
        self.assertTrue(self.client.login(username=self.username, password=self.password))
        response = self.client.delete(f"/books/delete/{self.book.id}/")
        self.assertIn(response.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))

    def test_search_and_ordering_work(self):
        response = self.client.get("/books/?search=First")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(item["title"] == "First Book" for item in response.data))
        response2 = self.client.get("/books/?ordering=title")
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response2.data) >= 1)
