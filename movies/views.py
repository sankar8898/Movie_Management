from rest_framework.decorators import api_view
from rest_framework.response import Response
from .omdb import search_movie, get_movie_details
from .serializers import MovieSerializer


@api_view(["GET"])
def search_movies(request):
    """
    Search movies by title using OMDb API and return basic info + details.
    """
    query = request.GET.get("q")
    if not query:
        return Response({"error": "Movie name required"}, status=400)

    data = search_movie(query)

    if "Error" in data:  # OMDb returns {"Response": "False", "Error": "..."}
        return Response({"error": data["Error"]}, status=404)

    results = []
    for m in data.get("Search", []):  # OMDb uses 'Search'
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
    Fetch a single movie’s full details from OMDb by imdbID.
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
