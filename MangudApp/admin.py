from django.contrib import admin
from . models import Game, GamePlatform, User

admin.site.register(Game)
admin.site.register(GamePlatform)
admin.site.register(User)
# Register your models here.
