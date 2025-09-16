from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .serializers import MovieSerializer


class MovieSerializerTest(TestCase):
    def test_movie_serializer(self):
        """Test that the serializer returns correct fields"""
        movie_data = {
            "id": "tt1375666",
            "title": "Inception",
            "poster": "https://example.com/inception.jpg",
            "rating": "8.8",
            "description": "A mind-bending thriller."
        }

        serializer = MovieSerializer(data=movie_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["title"], "Inception")
        self.assertEqual(serializer.validated_data["rating"], "8.8")


class MovieAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_search_movies_with_query(self):
        """Test that API returns results for a valid query"""
        response = self.client.get("/api/movies/search/?q=Inception")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("title", response.json()[0])  # Check first result has 'title'

    def test_search_movies_without_query(self):
        """Test that API returns error if query is missing"""
        response = self.client.get("/api/movies/search/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["error"], "Movie name required")
