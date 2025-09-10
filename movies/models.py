from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)  # TMDB movie ID
    title = models.CharField(max_length=255)
    poster = models.URLField(blank=True, null=True)
    rating = models.FloatField(default=0.0)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
