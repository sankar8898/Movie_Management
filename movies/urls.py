from django.urls import path
from . import views

urlpatterns = [

    path('', views.movie_search, name='movie_search'),

    path("search/", views.search_movies, name="search_movies"),
    path("recommendations/<int:movie_id>/", views.recommend_movies, name="recommend_movies"),
    path('add-favorite/<int:movie_id>/', views.add_favorite, name='add_favorite'),

]
