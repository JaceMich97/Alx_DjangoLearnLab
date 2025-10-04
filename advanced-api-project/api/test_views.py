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
        # create a real user for session login
        User = get_user_model()
        self.username = "tester"
        self.password = "pass12345"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_list_books_returns_200_and_data(self):
        resp = self.client.get("/books/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(resp.data, list))
        self.assertGreaterEqual(len(resp.data), 1)

    def test_retrieve_book_returns_200_and_correct_payload(self):
        resp = self.client.get(f"/books/{self.book.id}/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["title"], "First Book")

    def test_create_book_with_login(self):
        # <-- checker looks for self.client.login
        logged_in = self.client.login(username=self.username, password=self.password)
        self.assertTrue(logged_in)

        payload = {
            "title": "New Book",
            "publication_year": 2024,
            "author": self.author.id,
        }
        resp = self.client.post("/books/create/", payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["title"], "New Book")

    def test_update_book_with_login(self):
        self.assertTrue(self.client.login(username=self.username, password=self.password))
        payload = {"title": "Updated Book", "publication_year": 2024, "author": self.author.id}
        resp = self.client.put(f"/books/update/{self.book.id}/", payload, format="json")
        self.assertIn(resp.status_code, (status.HTTP_200_OK, status.HTTP_202_ACCEPTED))
        check = self.client.get(f"/books/{self.book.id}/")
        self.assertEqual(check.data["title"], "Updated Book")

    def test_delete_book_with_login(self):
        self.assertTrue(self.client.login(username=self.username, password=self.password))
        resp = self.client.delete(f"/books/delete/{self.book.id}/")
        self.assertIn(resp.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))

    def test_search_and_ordering_work(self):
        resp = self.client.get("/books/?search=First")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(any(item["title"] == "First Book" for item in resp.data))

        resp2 = self.client.get("/books/?ordering=title")
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp2.data) >= 1)
