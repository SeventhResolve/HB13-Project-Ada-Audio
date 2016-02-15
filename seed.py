from model import db, Artist, Song, Playlist, SongPlaylist
from pprint import pprint
from server import *

import os


def gets_json_from_apis():
    """If songs aren't in db, get the api jsons"""

    en_key = os.environ['ECHONEST_API_KEY']
    # yt_browser_key = os.environ['YOUTUBE_BROWSER_KEY']

    # search results from server.py
    artist_and_song = gets_user_search_results()

     # From request library, adds search to db
    en_payload = {'title': artist_and_song[1], 'artist': artist_and_song[0]}

    r = requests.get("http://developer.echonest.com/api/v4/song/search?api_key=%(en_key)s&format=json&results=1&" % locals(), params=en_payload)
    
    # Debugging print statement
    print (r.url)

    # binds dictionary from get request to variable
    dict_from_en_api = r.json()

    # Debugging print statement
    pprint(dict_from_en_api)

    parsed_search_results = parses_en_json_results(dict_from_en_api)


def adds_en_json_results_to_db(parsed_search_results):
    ''' Seeds the database with results from parses_en_json_results'''

    
    artist_info = Artist(en_artist_id=parsed_search_results[0],
                         artist_name=parsed_search_results[1])
    
    # checks for duplicate EN artist IDs
    while True:
        try:
            db.session.add(artist_info)
            db.session.commit()

            # for debugging
            print '######## Artist Tried'
            break
        except:
            
            # for debugging
            print "^^^^^^^^^Artist Breaked"
            break       


    song_info = Song(en_song_id=parsed_search_results[2],
                     song_title=parsed_search_results[3],
                     artist_id=artist_info.artist_id)

    # checks for duplicate EN song IDs
    while True:
        try:
            db.session.add(song_info)
            db.session.commit()

            # for debugging
            print '######## Song Tried'
            break
        except:
            
            # for debugging
            print "^^^^^^^^^ Song Breaked"
            break
