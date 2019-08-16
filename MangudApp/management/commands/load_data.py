from django.core.management.base import BaseCommand
import json, requests, time, calendar, math
from . secrets import api_key
from datetime import datetime

from MangudApp.models import Game, GamePlatform

class Command(BaseCommand):

    def handle(self, *args, **options):
        current_time = time.time()
        int_time= int(current_time)
        string_time =  str(int_time)
        
        url = 'https://api-v3.igdb.com/release_dates'
        params = "fields game.name, game.involved_companies.company.name, human, game.platforms.name, game.cover.url; where date > "+"1565644259"+"& game.platforms = (6, 46,48,130) ; sort date asc; limit 20;"
        response = requests.post(url, headers={'user-key': api_key}, data=params)
        data = json.loads(response.text)

        # get unique names
        games = []
        for i in range(len(data)):
            found = False
            for game in games:
                if game['name'] == data[i]['game']['name']:
                    found = True
            if not found:
                games.append(data[i]['game'])
                
        for game in games:
            g_name = game['name']
            if 'involved_companies' in game:
                for i in range(len(game['involved_companies'])):
                    if i == 0:
                        g_publisher = game['involved_companies'][i]['company']['name']
                    elif i == 1:
                        g_developer = game['involved_companies'][i]['company']['name']
            else:
                g_publisher = "Unknown"
                g_developer = "Unknown"
            release = data[i]['human']
            g_date_released = datetime.strptime(release, '%Y-%b-%d')
            
            g_platforms = game['platforms']
            
            if 'cover' in game:
                g_cover_url = "https:"+game['cover']['url']
            else:
                g_cover_url = "https://images.igdb.com/igdb/image/upload/t_thumb/nocover_qhhlj6.jpg"
            g_id = game['id'] 
        
            a_game = Game(title=g_name, publisher=g_publisher, developer=g_developer, release_date=g_date_released, igdb_id=g_id, cover_art_url=g_cover_url)
            a_game.save()
            for i in range(len(g_platforms)):
                platform, created = GamePlatform.objects.get_or_create(name=g_platforms[i]['name'])

                a_game.platforms.add(platform)
            
        