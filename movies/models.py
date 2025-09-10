from django.db import models

# Create your models here.

from django.db import models

class Movie(models.Model):
    tmdb_id = models.IntegerField(unique=True)  # TMDB movie ID
    title = models.CharField(max_length=255)
    poster = models.URLField(blank=True, null=True)
    rating = models.FloatField(default=0.0)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

