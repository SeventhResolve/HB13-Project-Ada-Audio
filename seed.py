from model import db, Artist, Song, Playlist, SongPlaylist
from pprint import pprint
from sqlalchemy import exists
# from sqlalchemy.orm import *

import requests
import os


def gets_json_from_en_api(artist_and_song):
    """If songs aren't in db, get the api jsons"""

    en_key = os.environ['ECHONEST_API_KEY']
    # yt_browser_key = os.environ['YOUTUBE_BROWSER_KEY']

    print "seed gets json from en api ", artist_and_song

    en_payload = {'title': artist_and_song[1], 'artist': artist_and_song[0]}

    r = requests.get("http://developer.echonest.com/api/v4/song/search?api_key=%(en_key)s&format=json&results=1&" % locals(), params=en_payload)
    
    # Debugging print statement
    print (r.url)

    # binds dictionary from get request to variable
    dict_from_en_api = r.json()

    # Debugging print statement
    pprint(dict_from_en_api)

    return dict_from_en_api

def parses_en_json_results(dict_from_en_api):
    ''' Parses EN JSON results'''

    artist_id = dict_from_en_api['response']['songs'][0]['artist_id']
    artist_name = dict_from_en_api['response']['songs'][0]['artist_name']
    song_id = dict_from_en_api['response']['songs'][0]['id']
    song_title = dict_from_en_api['response']['songs'][0]['title']

    # prints for debugging
    print artist_id
    print artist_name
    print song_id
    print song_title

    parsed_search_results = [artist_id, artist_name, song_id, song_title]

    return parsed_search_results



def adds_en_artist_results_to_db(parsed_search_results):
    ''' Seeds the database with artist results from parses_en_json_results'''

    new_artist_id = parsed_search_results[0]
    print new_artist_id

    if Artist.query.filter(Artist.en_artist_id == new_artist_id):
        print "Artist already exists"
    else:
        artist_info = Artist(en_artist_id=parsed_search_results[0],
                             artist_name=parsed_search_results[1])
        db.session.add(artist_info)
        db.session.flush()   
        print "Artist info successfully flushed"    


def adds_en_song_results_to_db(parsed_search_results):
    ''' Seeds the database with artist results from parses_en_json_results'''
    # This absolutely has to run AFTER adding artist to db. Required to
    # have artist to create foreign key

    print "Running adds_en_song_resuts_to_db"
    print "parsed_search_results ", parsed_search_results

    artist = parsed_search_results[1]
    en_artist_id = parsed_search_results[0]
    en_artist_id_str = str(en_artist_id)
    # convert to a string to query db

    is_artist_in_db = db.session.query(exists().where(Artist.artist_name==artist)).scalar()
    # checks to see if artist is already in db. Will luse db info if artist
    # is already in db. Will use EN API info if artist doesn't exist

    if is_artist_in_db == True:
        artist_id_result = db.session.query(Artist.artist_id).filter(Artist.en_artist_id == en_artist_id_str).one()
        # takes the EN artist id and queries for the primary key for that artist

        print ")))))))))))))) Returns a tuple"

        artist_id = artist_id_result[0]

        print "ARTIST-ID = ", artist_id

        song_info = Song(en_song_id=parsed_search_results[2],
                         song_title=parsed_search_results[3],
                         artist_id=artist_id)

        print "seed, adds en song resuts to db, ", artist_id
        
        db.session.add(song_info)
        db.session.flush()
        print "Song/Artist info successfully flushed"

    else:
        print "api helper adds_en_song_results_to_db !!!!!! Something went wrong adding artist to db!!!!!"

    


##############################################

# if __name__ == "__main__":

#     connect_to_db(app)
