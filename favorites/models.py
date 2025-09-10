from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to logged-in user
    movie_id = models.IntegerField()  # TMDB movie ID
    title = models.CharField(max_length=255)
    poster_url = models.URLField()
    rating = models.FloatField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user.username})"