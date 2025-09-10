from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Favorite

# Favorites page - shows all saved movies for the logged-in user
@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'favorites/favorites_list.html', {'favorites': favorites})

# Add a movie to favorites
@login_required
def add_to_favorites(request):
    if request.method == 'POST':
        movie_id = request.POST.get('movie_id')
        title = request.POST.get('title')
        poster_url = request.POST.get('poster_url')
        rating = request.POST.get('rating')
        description = request.POST.get('description')

        # Check if already exists
        favorite, created = Favorite.objects.get_or_create(
            user=request.user,
            movie_id=movie_id,
            defaults={
                'title': title,
                'poster_url': poster_url,
                'rating': rating,
                'description': description
            }
        )
        return redirect('favorites_list')  # Redirect to favorites page


# Create your views here.
@login_required
def remove_favorite(request, pk):
    favorite = get_object_or_404(Favorite, pk=pk, user=request.user)
    if request.method == 'POST':
        favorite.delete()
    return redirect('favorites_list')
