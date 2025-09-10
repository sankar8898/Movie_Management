from django.urls import path
from . import views

urlpatterns = [
    path('', views.favorites_list, name='favorites_list'),
    path('add/', views.add_to_favorites, name='add_to_favorites'),
    path('remove/<int:pk>/', views.remove_favorite, name='remove_favorite'),  # remove
]
