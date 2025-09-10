import os
import requests

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

def search_movie(query):
    url = f"{BASE_URL}/search/movie?api_key={TMDB_API_KEY}&query={query}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else {}

def get_recommendations(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}/recommendations?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    return response.json() if response.status_code == 200 else {}
