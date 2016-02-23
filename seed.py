from model import db, Artist, Song, Playlist, SongPlaylist
from pprint import pprint
from sqlalchemy import exists
# from sqlalchemy.orm import *

import requests
import os


def gets_json_from_en_api(artist_and_song):
    """If songs aren't in db, get the api jsons"""

    en_key = os.environ['ECHO_NEST_API_KEY']
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

    en_artist_id = parsed_search_results[0]
    print en_artist_id

    is_artist_in_db = db.session.query(exists().where(Artist.en_artist_id==en_artist_id)).scalar()

    if is_artist_in_db == True:
        print "Seed, Artist already exists"
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
    # RETURNS artist_id to be added to YT table

    print "Running adds_en_song_resuts_to_db"
    print "parsed_search_results ", parsed_search_results

    en_song_id = parsed_search_results[2]
    en_song_id_str = str(en_song_id)    # needs to be in string format to query db
    song_title = parsed_search_results[3]

    artist = parsed_search_results[1]
    en_artist_id = parsed_search_results[0]
    en_artist_id_str = str(en_artist_id)    # needs to db in string format to query db

    is_artist_en_id_in_db = db.session.query(exists().where(Artist.en_artist_id == en_artist_id_str)).scalar()
    # checks to see if artist's en_id is already in db. Will use db info if artist
    # is already in db. Will use EN API info if artist doesn't exist. Previous 
    # queries checked artist as a STRING
    is_song_en_id_in_db = db.session.query(exists().where(Song.en_song_id == en_song_id_str)).scalar()
    # checks to see if song's en_id is already in db. If en_id exists, song is 
    # in db. If it doesn't, add artist. Previous queries checked song as a 
    # STRING

    if is_song_en_id_in_db == True:
        print "seed, adds_en_song_resuts_to_db, Song's EN ID in DB"
        artist_id_result = db.session.query(Artist.artist_id).filter(Artist.en_artist_id == en_artist_id_str).one()
        # takes the EN artist id and queries for the primary key for that artist

        artist_id = artist_id_result[0]

        return artist_id
    else:
        if is_artist_en_id_in_db == True:
            artist_id_result = db.session.query(Artist.artist_id).filter(Artist.en_artist_id == en_artist_id_str).one()
            # takes the EN artist id and queries for the primary key for that artist

            artist_id = artist_id_result[0]

            song_info = Song(en_song_id=en_song_id,
                         song_title=song_title,
                         artist_id=artist_id)

            print "seed, adds en song resuts to db, ", artist_id
            
            db.session.add(song_info)
            db.session.flush()
            print "Song/Artist info successfully flushed"
            return artist_id

        else:
            print """seed, adds_en_song_resuts_to_db, artist with same
                  name exists but en_id is new. Add artist and song to db."""

            artist_info = Artist(en_artist_id=parsed_search_results[0],
                                 artist_name=parsed_search_results[1])

            db.session.add(artist_info)
            db.session.flush()   
            print "seed, adds_en_song_resuts_to_db, Artist info successfully flushed" 

            song_info = Song(en_song_id=en_song_id,
                         song_title=song_title,
                         artist_id=artist_id)

            db.session.add(song_info)
            db.session.flush()
            print "seed, adds_en_song_resuts_to_db, Artist and Song added"
            return artist_id

    


##############################################

# if __name__ == "__main__":

#     connect_to_db(app)
