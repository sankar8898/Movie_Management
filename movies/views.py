from django.shortcuts import render
import requests

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
