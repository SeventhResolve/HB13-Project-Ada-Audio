# from apiclient.discovery import build
# from apiclient.errors import HttpError
# from oauth2client.tools import argparser
from model import db, Artist, Song, Playlist, SongPlaylist
from sqlalchemy import *
from sqlalchemy.orm import *

import os

def song_query_db(artist_and_song):
    """Takes the song, queries db for duplicates"""

    song = artist_and_song[1]

    # returns True or false if artist or song is in db
    is_song_in_db = db.session.query(exists().where(Song.song_title==song)).scalar()

    # Debugging
    print "Is song in db? %s" % (is_song_in_db)

    if is_song_in_db == True:
        # Debugging
        print "This song is in the db", song

    else:
        # add song's YT and EN ID's to database
        return query_song_apis(song)


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

def query_song_apis(song_str):

    # Debugging
    print "Got to query_song_api fn"

    

def parses_en_json_results(dict_from_en_api):

    ''' *** From a song/artist search ***
    1. takes the json dictionary from turns_search_into_en_dict from server.py
    parses through the dictionary
    2. pulls out artist_id, artist, song, and song_id.
    3. adds each item to the add_to_database
    '''

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

def parses_yt_json_results(dict_from_yt_api):

    pass
