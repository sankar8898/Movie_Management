from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Movie, Favorite
from .omdb import search_movie, get_movie_details
from .serializers import MovieSerializer
import requests


# -------------------------
# Template views
# -------------------------
def movie_list(request):
    """Show all movies saved in DB."""
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})


def movie_search(request):
    """Search movies using TMDB API (front-end form)."""
    movies = []
    query = request.GET.get('q')  # from ?q=
    if query:
        api_key = "YOUR_TMDB_API_KEY"
        url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={query}"
        response = requests.get(url)
        data = response.json()
        results = data.get('results', [])
        for movie in results:
            movies.append({
                'id': movie['id'],
                'title': movie['title'],
                'poster_url': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else "",
                'rating': movie.get('vote_average'),
                'description': movie.get('overview'),
            })
    return render(request, 'movies/movie_list.html', {'movies': movies})


@login_required
def add_favorite(request, movie_id):
    """Save movie as favorite for logged-in user."""
    movie = get_object_or_404(Movie, id=movie_id)
    Favorite.objects.get_or_create(user=request.user, movie=movie)
    return redirect('movie_list')


# -------------------------
# API views (DRF)
# -------------------------
@api_view(["GET"])
def search_movies(request):
    """
    Search movies by title using OMDb API.
    """
    query = request.GET.get("q")
    if not query:
        return Response({"error": "Movie name required"}, status=400)

    data = search_movie(query)

    if "Error" in data:
        return Response({"error": data["Error"]}, status=404)

    results = []
    for m in data.get("Search", []):
        details = get_movie_details(m["imdbID"])
        results.append({
            "id": m.get("imdbID"),
            "title": m.get("Title", "Unknown"),
            "poster": m.get("Poster", ""),
            "rating": details.get("imdbRating", "N/A"),
            "description": details.get("Plot", "No description available"),
            "year": m.get("Year", "Unknown"),
            "type": m.get("Type", "movie")
        })

    serializer = MovieSerializer(results, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def movie_details(request, imdb_id):
    """
    Fetch full movie details by imdbID from OMDb.
    """
    details = get_movie_details(imdb_id)

    if details.get("Response") == "False":
        return Response({"error": details.get("Error", "Movie not found")}, status=404)

    result = {
        "id": details.get("imdbID"),
        "title": details.get("Title", "Unknown"),
        "poster": details.get("Poster", ""),
        "rating": details.get("imdbRating", "N/A"),
        "description": details.get("Plot", "No description available"),
        "genre": details.get("Genre", ""),
        "director": details.get("Director", ""),
        "actors": details.get("Actors", ""),
        "year": details.get("Year", "Unknown"),
        "runtime": details.get("Runtime", "")
    }

    return Response(result)


