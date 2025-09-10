import os
import requests
from django.conf import settings

TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_API_KEY = settings.TMDB_API_KEY

def search_movie(query):
    url = f"{TMDB_BASE_URL}/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": query}
    response = requests.get(url, params=params)
    return response.json()

def get_recommendations(movie_id):
    url = f"{TMDB_BASE_URL}/movie/{movie_id}/recommendations"
    params = {"api_key": TMDB_API_KEY}
    response = requests.get(url, params=params)
    return response.json()
