
from django.shortcuts import render
from .models import Movie, Favorite
import requests
def movie_search(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})
def movie_search(request):
    movies = []
    query = request.GET.get('q')  # Get search term from URL ?q=
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


# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tmdb import search_movie, get_recommendations
from .serializers import MovieSerializer
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Movie, Favorite
@api_view(['GET'])
def search_movies(request):
    query = request.GET.get("q")
    if not query:
        return Response({"error": "Movie name required"}, status=400)

    data = search_movie(query)
    if not data or "results" not in data:
        return Response({"error": "TMDB API error"}, status=502)

    results = []
    for m in data.get("results", []):
        results.append({
            "id": m.get("id"),
            "title": m.get("title"),
            "poster": f"https://image.tmdb.org/t/p/w500{m['poster_path']}" if m.get("poster_path") else "",
            "rating": m.get("vote_average", 0.0),
            "description": (m.get("overview", "")[:150] + "...") if m.get("overview") else "No description",
        })

    serializer = MovieSerializer(results, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def recommend_movies(request, movie_id):
    data = get_recommendations(movie_id)
    if not data or "results" not in data:
        return Response({"error": "TMDB API error"}, status=502)

    results = []
    for m in data.get("results", []):
        results.append({
            "id": m.get("id"),
            "title": m.get("title"),
            "poster": f"https://image.tmdb.org/t/p/w500{m['poster_path']}" if m.get("poster_path") else "",
            "rating": m.get("vote_average", 0.0),
            "description": (m.get("overview", "")[:150] + "...") if m.get("overview") else "No description",
        })

    serializer = MovieSerializer(results, many=True)
    return Response(serializer.data)

@login_required
def add_favorite(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    Favorite.objects.get_or_create(user=request.user, movie=movie)
    return redirect('movie_list')
def movie_list(request):
    movies = Movie.objects.all()
    return render(request, 'movies/movie_list.html', {'movies': movies})