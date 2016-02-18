# from apiclient.discovery import build
# from apiclient.errors import HttpError
# from oauth2client.tools import argparser
from model import db, Artist, Song, Playlist, SongPlaylist
from sqlalchemy import exists
from sqlalchemy.orm import *
from seed import *

# import os
# import requests
import json

def queries_song_db(artist_and_song):
    """Takes the song, queries db for duplicates and adds unique enteries"""
    # Logic: The song/artist is assumed to be unique. Query for the song title
    # if the song title exists, check if the song's artist is the same as the artist
    # the user searched for. If the artist is different, the song is not in the
    # database and must be added. If the artist is the same, the song is already
    # in the database

    print "api_helper queries_song_db started"
    artist = artist_and_song[0]
    song = artist_and_song[1]

    is_song_in_db = db.session.query(exists().where(Song.song_title == song)).scalar()

    # Debugging
    print "api_helper Is song in db? %s" % (is_song_in_db)
 
    if is_song_in_db == True:
        # If song is in db, check if song has same artist_id as searched artist
        
        list_of_songs = db.session.query(Song.song_title).filter(Song.song_title == song).all()
        # Query to see if song's artist_id and the artist artist_id matches
        # this returns a list
        
        print "results from is song in db query ", songs 

        for each_song in list_of_songs:
            if each_song.artist.artist_name == artist:
                print "Song artist combo in db :D :D :D :D"
                return "In db"

            else:
                print "Song/artist combo doesn't exist add to db"
            return "Add to db"
    else:
        print "api_helper populating db"
        return "Add to db"

def song_populate_database(artist_and_song):
    """Adds song to db using seed.py"""

    print "populating db! with ", artist_and_song

    step_one = gets_json_from_en_api(artist_and_song)
    print "api helper, populate_database Step one complete!"
    step_two = parses_en_json_results(step_one)
    print "api helper, populate_database Step two complete!"
    step_three = adds_en_artist_results_to_db(step_two)
    print "api helper, populate_database Step three complete!"
    step_four = adds_en_song_results_to_db(step_two)
    print "api helper, populate_database Step four complete!"

    return "api helper Song and artist info added to db"

def queries_artist_db(artist_and_song):
    """Takes the artist, queries db for duplicates"""

    # from server.py
    artist = artist_and_song[0]


    # returns True or false if artist or song is in db
    is_artist_in_db = db.session.query(exists().where(Artist.artist_name==artist)).scalar()

    # Debugging
    print "is_artist_in_db", is_artist_in_db

    if is_artist_in_db == False:
        print "api helper queries_artist_db OOPS artist isn't in db"
        return "False"
    else:
        print "api helper queries_artist_db HEY artist is in db"
        return "True"


def artist_populate_database(artist_and_song):
    """ Adds new artist to db """
    
    step_one = gets_json_from_en_api(artist_and_song)
    step_two = parses_en_json_results(step_one)
    step_three = adds_en_artist_results_to_db(step_two)

    print "api helper artist_populate_database, new artist added to db"






