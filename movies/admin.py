from django.contrib import admin

# Register your models here.
<<<<<<< HEAD
=======
from django.contrib import admin
from .models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'rating')
>>>>>>> origin/feature/geeta
