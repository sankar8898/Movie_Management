import os
import requests
from dotenv import load_dotenv

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")
BASE_URL = "http://www.omdbapi.com/"

def search_movie(query):
    """Search movie by title"""
    params = {
        "apikey": OMDB_API_KEY,
        "s": query  # 's' is search parameter in OMDb
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()

def get_movie_details(imdb_id):
    """Get full details of a movie by IMDb ID"""
    params = {
        "apikey": OMDB_API_KEY,
        "i": imdb_id,
        "plot": "short"
    }
    response = requests.get(BASE_URL, params=params)
    return response.json()
