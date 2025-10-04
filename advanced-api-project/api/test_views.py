from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import Author, Book


class BookAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Base data used across tests
        cls.author = Author.objects.create(name="Isaac Asimov")
        cls.other_author = Author.objects.create(name="Ursula Le Guin")

        cls.book1 = Book.objects.create(
            title="Foundation",
            publication_year=1951,
            author=cls.author,
        )
        cls.book2 = Book.objects.create(
            title="The Left Hand of Darkness",
            publication_year=1969,
            author=cls.other_author,
        )

        # A user for authenticated endpoints
        User = get_user_model()
        cls.user = User.objects.create_user(
            username="tester", password="pass1234"
        )

    def setUp(self):
        self.client = APIClient()

    # ---------- READ (no auth required) ----------
    def test_book_list_returns_200(self):
        resp = self.client.get("/api/books/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in resp.json()]
        self.assertIn(self.book1.title, titles)
        self.assertIn(self.book2.title, titles)

    def test_book_detail_returns_200(self):
        resp = self.client.get(f"/api/books/{self.book1.pk}/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.json()["title"], self.book1.title)

    # ---------- CREATE / UPDATE / DELETE (auth required) ----------
    def test_create_requires_auth_then_creates(self):
        # Unauthenticated should be forbidden
        resp = self.client.post(
            "/api/books/create/",
            {"title": "New Book", "publication_year": 2024, "author": self.author.id},
            format="json",
        )
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

        # Authenticated -> 201
        self.client.login(username="tester", password="pass1234")
        resp = self.client.post(
            "/api/books/create/",
            {"title": "New Book", "publication_year": 2024, "author": self.author.id},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Book.objects.filter(title="New Book").exists())

    def test_update_book_authenticated(self):
        self.client.login(username="tester", password="pass1234")
        resp = self.client.put(
            f"/api/books/update/{self.book1.pk}/",
            {"title": "Foundation (Updated)", "publication_year": 1951, "author": self.author.id},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Foundation (Updated)")

    def test_delete_book_authenticated(self):
        self.client.login(username="tester", password="pass1234")
        resp = self.client.delete(f"/api/books/delete/{self.book2.pk}/")
        # DRF DestroyAPIView returns 204 by default
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book2.pk).exists())

    # ---------- Filter / Search / Ordering ----------
    def test_search_and_ordering_and_filter(self):
        # search by author name
        resp = self.client.get("/api/books/?search=Asimov")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in resp.json()]
        self.assertIn("Foundation", titles)

        # ordering by publication_year asc
        resp = self.client.get("/api/books/?ordering=publication_year")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in resp.json()]
        self.assertEqual(years, sorted(years))

        # filter by exact year
        resp = self.client.get("/api/books/?publication_year=1969")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(all(b["publication_year"] == 1969 for b in resp.json()))
