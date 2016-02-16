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

    artist = artist_and_song[0]
    song = artist_and_song[1]

    is_song_in_db = db.session.query(exists().where(Song.song_title==song)).scalar()

    # Debugging
    print "api_helper Is song in db? %s" % (is_song_in_db)
 
    if is_song_in_db == True:
        # If song is in db, check if song has same artist_id as searched artist
        
        # Query to see if song's artist_id and the artist artist_id matches
        song_artist_ids = db.session.query(Song.artist_id).filter(Song.song_title==song).all()
        artist_ids = db.session.query(Artist.artist_id).filter(Artist.artist_name==artist).all()

        contains_true_or_false = []

        for item in song_artist_ids:
            song_artist_id = item[0]
            for item in artist_ids:
                artist_id = item[0]
                # This get all the possible artist/song combos
                print "song_artist_id ",  song_artist_id, " artist_id ", artist_id

                # Checks to see if this particular combo of song's artist_id 
                # matches the artist's artist_id then adds the boolean to a list
                song_artist_bool = (song_artist_id == artist_id)
                contains_true_or_false.append(song_artist_bool)

                print contains_true_or_false

        # If the list contains a True value, the song exists in the db.
        # If the list is all False then the search is a unique song/artist combo  
        if any(contains_true_or_false) == True:
            print "Super uber checked. Song exists in db."
            # return "Render playlist/video"
        else:
            print "Super uber checked. Song/artist combo doesn't exist in db."
            return artist_and_song
    else:
        print "api_helper populating db"
        return artist_and_song

def populate_database(artist_and_song):
    """Adds song to db using seed.py"""
    print "populating db!"

    step_one = gets_json_from_en_api(artist_and_song)
    print "api helper, populate_database Step one complete!"
    step_two = parses_en_json_results(step_one)
    print "api helper, populate_database Step two complete!"
    step_three = adds_en_json_results_to_db(step_two)
    print "api helper, populate_database Step three complete!"


    return "api helper Song and artist info added to db"

def artist_query_db(artist_and_song):
    """Takes the artist, queries db for duplicates"""

    # from server.py
    artist = artist_and_song[0]


    # returns True or false if artist or song is in db
    is_artist_in_db = db.session.query(exists().where(Artist.artist_name==artist)).scalar()

    # Debugging
    print is_artist_in_db

    if is_artist_in_db == False:
        return artist
    else:
        # add artist's EN ID to database
        return query_artist_en_id(artist)

