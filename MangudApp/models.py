from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    on_newsletter = models.BooleanField(default=False)

class GamePlatform(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class Game(models.Model):
    title = models.CharField(max_length = 500)
    developer = models.CharField(max_length = 200)
    publisher = models.CharField(max_length = 200)
    platforms = models.ManyToManyField(GamePlatform)
    release_date = models.DateField()
    cover_art_url = models.CharField(max_length = 500)
    igdb_id = models.CharField(max_length = 8)
    user_wishlist = models.ManyToManyField(User, related_name='saved_games')
    

    def __str__(self):
        return self.title
