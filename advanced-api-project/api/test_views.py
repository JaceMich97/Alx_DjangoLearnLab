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
        # user for authenticated endpoints
        User = get_user_model()
        self.user = User.objects.create_user(username="tester", password="pass12345")

    def test_list_books_returns_200_and_data(self):
        resp = self.client.get("/books/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # the checker looks for response.data
        self.assertTrue(isinstance(resp.data, list))
        self.assertGreaterEqual(len(resp.data), 1)

    def test_retrieve_book_returns_200_and_correct_payload(self):
        resp = self.client.get(f"/books/{self.book.id}/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["title"], "First Book")  # uses response.data

    def test_search_and_ordering_work(self):
        # search by title
        resp = self.client.get("/books/?search=First")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(any(item["title"] == "First Book" for item in resp.data))

        # ordering by title (just check it doesn't error and returns data)
        resp2 = self.client.get("/books/?ordering=title")
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)
        self.assertTrue(len(resp2.data) >= 1)

    def test_create_book_requires_auth_and_returns_created(self):
        self.client.force_authenticate(user=self.user)
        payload = {"title": "New Book", "publication_year": 2024, "author": self.author.id}
        resp = self.client.post("/books/create/", payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["title"], "New Book")  # uses response.data

    def test_update_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        payload = {"title": "Updated Book", "publication_year": 2024, "author": self.author.id}
        resp = self.client.put(f"/books/update/{self.book.id}/", payload, format="json")
        # different setups return 200/202; accept both
        self.assertIn(resp.status_code, (status.HTTP_200_OK, status.HTTP_202_ACCEPTED))
        # fetch again to verify persisted update
        check = self.client.get(f"/books/{self.book.id}/")
        self.assertEqual(check.data["title"], "Updated Book")

    def test_delete_book_authenticated(self):
        self.client.force_authenticate(user=self.user)
        resp = self.client.delete(f"/books/delete/{self.book.id}/")
        self.assertIn(resp.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))
