# from apiclient.discovery import build
# from apiclient.errors import HttpError
# from oauth2client.tools import argparser
from model import db, Artist, Song, Playlist, SongPlaylist
from sqlalchemy import *
from sqlalchemy.orm import *
from seed import *

# import os
# import requests
import json

def queries_song_db(artist_and_song):
    """Takes the song, queries db for duplicates and adds unique enteries"""

    song = artist_and_song[1]

    # returns True or false if artist or song is in db
    is_song_in_db = db.session.query(exists().where(Song.song_title==song)).scalar()

    # Debugging
    print "api_help Is song in db? %s" % (is_song_in_db)

    if is_song_in_db == True:
        # Debugging
        print "api_help This song is in the db", song
        return is_song_in_db
    else:
        # add song's YT and EN ID's to database
        return adds_artist_and_song_to_db(artist_and_song)

def adds_artist_and_song_to_db(artist_and_song):
    """Adds song to db using seed.py"""
    step_one = gets_json_from_apis(artist_and_song)
    step_two = parses_en_json_results(step_one)
    step_three = adds_en_json_results_to_db(step_two)

    print "api help Song and artist info added to db"

def artist_query_db(artist_and_song):
    """Takes the artist, queries db for duplicates"""

    # from server.py fn=
    artist = artist_and_song[0]


    # returns True or false if artist or song is in db
    is_artist_in_db = db.session.query(exists().where(Artist.artist_name==artist)).scalar()

    # Debugging
    print is_artist_in_db

    if is_artist_in_db == True:
        return artist
    else:
        # add artist's EN ID to database
        return query_artist_en_id(artist)

# def query_song_apis(artist, song):

#     # Debugging
#     print "Got to query_song_api fn"

#     payload = {'title': song, 'artist': artist}

#     r = requests.get("http://developer.echonest.com/api/v4/song/search?api_key=%(en_key)s&format=json&results=1&" % locals(), params=payload)
    
#     # Debugging print statement
#     print (r.url)

#     # binds dictionary from get request to variable
#     dict_from_en_api = r.json()

#     # Debugging print statement
#     pprint(dict_from_en_api)

# def parses_en_json_results(dict_from_en_api):

#     ''' *** From a song/artist search ***
#     1. takes the json dictionary from turns_search_into_en_dict from server.py
#     parses through the dictionary
#     2. pulls out artist_id, artist, song, and song_id.
#     3. adds each item to the add_to_database
#     '''

#     artist_id = dict_from_en_api['response']['songs'][0]['artist_id']
#     artist_name = dict_from_en_api['response']['songs'][0]['artist_name']
#     song_id = dict_from_en_api['response']['songs'][0]['id']
#     song_title = dict_from_en_api['response']['songs'][0]['title']

#     # prints for debugging
#     print artist_id
#     print artist_name
#     print song_id
#     print song_title

#     parsed_search_results = [artist_id, artist_name, song_id, song_title]

#     return parsed_search_results

# def parses_yt_json_results(dict_from_yt_api):

#     pass
