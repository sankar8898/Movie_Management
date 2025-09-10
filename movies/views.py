from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tmdb import search_movie, get_recommendations
from .serializers import MovieSerializer

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
