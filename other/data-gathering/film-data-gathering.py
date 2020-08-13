
import string
import utils
import requests
import json

MAX_PAGE = 20

api_key = ''

base_img_url = 'https://image.tmdb.org/t/p/w500/'

db = utils.database_connect()
cursor = db.cursor()

with open('./other/tmdb-api.txt') as f:
    api_key = f.readline()
    print('API KEY: ' + api_key)

for i in range(1, MAX_PAGE+1):
    r = requests.get('https://api.themoviedb.org/3/movie/top_rated?api_key=' + api_key + '&language=en-US&page=' + str(i))
    
    response = r.json()
    for film in response['results']:
        if film['genre_ids'].__contains__(16) and film['original_language'] == 'ja': # japanese animated movies
            if film['vote_count'] >= 2500:
                filename = utils.download_image(base_img_url + film['poster_path'])
                cursor.execute('INSERT INTO images (year, path, event_name, img_caption, category) VALUES (%s, %s, %s, %s, %s)', (film['release_date'][:4], filename, film['title'], '', 'Anime'))
                db.commit()
        else:
            if film['vote_count'] >= 7500: # general famous movies
                filename = utils.download_image(base_img_url + film['poster_path'])
                cursor.execute('INSERT INTO images (year, path, event_name, img_caption, category) VALUES (%s, %s, %s, %s, %s)', (film['release_date'][:4], filename, film['title'], '', 'Film'))
                db.commit()


    q = requests.get('https://api.themoviedb.org/3/tv/top_rated?api_key=' + api_key + '&language=en-US&page=' + str(i))
    response = q.json()
    for tv_show in response['results']:
        if tv_show['original_language'] == 'ja' and tv_show['vote_count'] > 200 and tv_show['genre_ids'].__contains__(16): # japanese anime
            filename = utils.download_image(base_img_url + tv_show['poster_path'])
            cursor.execute('INSERT INTO images (year, path, event_name, img_caption, category) VALUES (%s, %s, %s, %s, %s)', (tv_show['first_air_date'][:4], filename, tv_show['name'], '', 'Anime'))
            db.commit()
        elif tv_show['vote_count'] > 1500: # other famous tv shows (GoT, Breaking Bad, ....)
            filename = utils.download_image(base_img_url + tv_show['poster_path'])
            cursor.execute('INSERT INTO images (year, path, event_name, img_caption, category) VALUES (%s, %s, %s, %s, %s)', (tv_show['first_air_date'][:4], filename, tv_show['name'], '', 'TV Show'))
            db.commit()