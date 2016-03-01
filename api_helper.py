from model import db, Artist, Song, Playlist, SongPlaylist
from sqlalchemy import exists
from sqlalchemy.orm import *
from seed import *
from pyechonest import *
from youtube import *

import json
import requests




def adds_unique_searches_to_database(artist_and_song):
    """Combines several functions to query db for duplicates and adds missing songs and/or artist"""

    artist = artist_and_song[0]
    song = artist_and_song[1]
    
    is_artist_in_db_query = queries_artist_db(artist_and_song)
    if is_artist_in_db_query == False:
        adds_artist_to_db = artist_populate_database(artist_and_song)
        returns_artist_id = song_populate_database(artist_and_song)
        print "server, artist added to db"
        return returns_artist_id
    else:
        song_query_results = queries_song_db(artist_and_song)
        if song_query_results == "In db":
            print "Song is in db, retrieving artist_id"

            song_artist_ids = db.session.query(Song.artist_id).filter(Song.song_title==song).all()
            artist_ids = db.session.query(Artist.artist_id).filter(Artist.artist_name==artist).all()

            for item in song_artist_ids:
                song_artist_id = item[0]
                for item in artist_ids:
                    artist_id = item[0]
                    
                    if song_artist_id == artist_id:
                        print "api_helper, adds_unique_searches_to_database returns_artist_id ", artist_id
                        returns_artist_id = artist_id
                        return returns_artist_id

        elif song_query_results == "Add to db":
            returns_artist_id = song_populate_database(artist_and_song)
            print "server gets_user_serach_results database populated"
            db.session.commit()    
            return returns_artist_id
        

def queries_artist_db(artist_and_song):
    """Takes the artist, queries db for duplicates"""

    # from server.py
    artist = artist_and_song[0]


    # returns True or false if artist or song is in db
    is_artist_in_db = db.session.query(exists().where(Artist.artist_name==artist)).scalar()

    # Debugging
    print "is_artist_in_db", is_artist_in_db

    if is_artist_in_db == False:
        print """api helper queries_artist_db OOPS artist isn't in db so
                 song is not in db either. Add both."""
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
            

def queries_song_db(artist_and_song):
    """Takes the song, queries db for duplicates and adds unique enteries"""
    # Logic: The song/artist is assumed to be unique. Query for the song title.
    # If the song title exists, check if the song's artist is the same as the artist
    # the user searched for. If the artist is different, the song is not in the
    # database and must be added. If the artist is the same, the song is already
    # in the database

    print "api_helper queries_song_db started"
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
            return "In db"
        else:
            print "Super uber checked. Song/artist combo doesn't exist in db."
            return "Add to db"
    else:
        print "api_helper Song not in db. Need to populate db"
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
    returns_artist_id = adds_en_song_results_to_db(step_two)
    print "api helper, populate_database Step four complete!"

    return returns_artist_id


def creates_en_playlist(en_session_id_and_en_song_id):
    """Generates an EchoNest playlist to query YouTube"""
    # get parameter from seed.py

    en_playlist = playlist.Playlist(session_id=en_session_id_and_en_song_id[0],
                                 song_id=en_session_id_and_en_song_id[1])
    print "Echonest playlist ", en_playlist

    en_song_id = en_session_id_and_en_song_id[1]

    en_playlist_and_seed_en_song_id = [en_playlist, en_song_id]

    return en_playlist_and_seed_en_song_id


def gets_playlist_history(en_playlist_and_seed_en_song_id):

    en_playlist = en_playlist_and_seed_en_song_id[0]

    current_song = en_playlist.get_current_songs()
    print "Current song ", current_song

    next_song = en_playlist.get_next_songs(results=5)
    print "Next songs ", next_song
    # this returns a list of songs names (doesn't seem all that useful)

    playlist_info_content = en_playlist.info()
    print "Playlist info ", pprint(playlist_info_content)
    # prints a dictionary with the playlist history

    playlist_history = playlist_info_content['history']
    # list of songs with song info as a dictionary

    en_song_id = en_playlist_and_seed_en_song_id[1]

    print "ECHONEST SONG ID ********** ", en_song_id
    # get seed song info to add as first song in playlist
    song_object = Song.query.filter(Song.en_song_id == en_song_id).one()
    artist_id = song_object.artist_id
    
    en_artist_id = db.session.query(Artist.en_artist_id).filter(Artist.artist_id == artist_id).one()            
    en_artist_id = en_artist_id[0]
    
    artist_name = db.session.query(Artist.artist_name).filter(Artist.artist_id == artist_id).one()            
    artist_name = artist_name[0]

    song_title = db.session.query(Song.song_title).filter(Song.en_song_id == en_song_id).one()
    song_title = song_title[0]

    yt_playlist_query = [{'artist_name': artist_name,
                         'en_artist_id': en_artist_id,
                         'song_title': song_title,
                         'en_song_id': en_song_id}]

    for each_song in playlist_history:
        artist_name = each_song['artist_name']
        en_artist_id = each_song['artist_id']
        song_title = each_song['title']
        en_song_id = each_song['id']

        yt_song_query = {'artist_name': artist_name, 
                         'en_artist_id': en_artist_id, 
                         'song_title': song_title,
                         'en_song_id': en_song_id}

        yt_playlist_query.append(yt_song_query)

    print "++++++++++++++++++ ", yt_playlist_query
    # list of current song and the next 5 songs that will play
    return yt_playlist_query


def creates_yt_playlist_query(artist_and_song):
    """Creates an en playlist"""
    # parsed_search_results from seed.py, parses_en_json_results(dict_from_en_api)

    step_one = gets_json_from_en_api(artist_and_song)
    step_two = parses_en_json_results(step_one)
    en_session_id_and_en_song_id = generates_en_playlist_session_id(step_two)
    adds_en_session_id_to_db(en_session_id_and_en_song_id)
    db.session.flush()
    en_playlist_and_seed_en_song_id = creates_en_playlist(en_session_id_and_en_song_id)
    yt_playlist_query = gets_playlist_history(en_playlist_and_seed_en_song_id)
    # list of current song and the next 5 songs that will play
    # in [[artist_name, title], []] format

    print "))))))))))))))))))) ", yt_playlist_query

    return yt_playlist_query










