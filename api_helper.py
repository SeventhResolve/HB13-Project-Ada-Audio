from model import db, Artist, Song, Playlist, SongPlaylist
from sqlalchemy import exists
from sqlalchemy.orm import *
from seed import *
from pyechonest import *
from youtube import *

import json
import requests
import os



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

    return en_playlist


def gets_playlist_history(en_playlist):

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

    yt_playlist_query = []
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

    print yt_playlist_query
    # list of current song and the next 5 songs that will play
    return yt_playlist_query


def creates_yt_playlist_query(artist_and_song):
    """ Asdf """
    # parsed_search_results from seed.py, parses_en_json_results(dict_from_en_api)

    step_one = gets_json_from_en_api(artist_and_song)
    step_two = parses_en_json_results(step_one)
    en_session_id_and_en_song_id = generates_en_playlist_session_id(step_two)
    adds_en_session_id_to_db(en_session_id_and_en_song_id)
    en_playlist = creates_en_playlist(en_session_id_and_en_song_id)
    yt_playlist_query = gets_playlist_history(en_playlist)
    # list of current song and the next 5 songs that will play
    # in [[artist_name, title], []] format

    return yt_playlist_query

def adds_youtube_playlist_videos_to_db(yt_playlist_query):
    """Takes the list of songs and finds the coresponding music video"""

    for item in yt_playlist_query:

        artist_name = item['artist_name']
        song_title = item['song_title']
        artist_and_song = [artist_name, song_title]

        dict_from_yt_api = yt_api_call(artist_and_song)
        parsed_search_results = parses_yt_results(dict_from_yt_api)

        contains_artist_name_and_artist_id = []
        en_song_id = item['en_song_id']
        print("en_song_id ", en_song_id)
        artist_name_and_artist_id = db.session.query(Artist.artist_name, Artist.artist_id).filter(Song.en_song_id == en_song_id).one()
        contains_artist_name_and_artist_id.append(artist_name_and_artist_id)

        contains_video_ids = []
        for each_artist_name_and_artist_id in contains_artist_name_and_artist_id:
            artist_name = each_artist_name_and_artist_id[0]
            if artist_name == each_artist_and_song[0]:
                artist_id = each_artist_name_and_artist_id[1]
                video_id = parsed_search_results[video_id]
                contains_video_ids.append(video_id)
                adds_yt_video_info_to_db(parsed_search_results, each_artist_and_song, artist_id)

    print "api_helper, adds_youtube_playlist_videos_to_db, contains_video_ids ", contains_video_ids
    return contains_video_ids


def makes_playlist_of_yt_video_ids(contains_video_ids):
    """Queries Youtube Video db and creates a playlist with video ids"""
    # Parameter in list form

    return contains_video_ids


def create_yt_playlist_id():
    
    import httplib2
    import os
    import sys
    import json

    from apiclient.discovery import build
    from apiclient.errors import HttpError
    from oauth2client.client import flow_from_clientsecrets
    from oauth2client.file import Storage
    from oauth2client.tools import argparser, run_flow

    # *** Following code provided by the YouTube API***
    # The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
    # the OAuth 2.0 information for this application, including its client_id and
    # client_secret. You can acquire an OAuth 2.0 client ID and client secret from
    # the Google Developers Console at
    # https://console.developers.google.com/.
    # Please ensure that you have enabled the YouTube Data API for your project.
    # For more information about using OAuth2 to access the YouTube Data API, see:
    #   https://developers.google.com/youtube/v3/guides/authentication
    # For more information about the client_secrets.json file format, see:
    #   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
    CLIENT_SECRETS_FILE = "/Users/Kitty/HB13/ada_audio/client_secrets.json"


    # This variable defines a message to display if the CLIENT_SECRETS_FILE is
    # missing.
    MISSING_CLIENT_SECRETS_MESSAGE = """
    WARNING: Please configure OAuth 2.0

    To make this sample run you will need to populate the client_secrets.json file
    found at:

     %s

    with information from the Developers Console
    https://console.developers.google.com/

    For more information about the client_secrets.json file format, please visit:
    https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
    """ % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                     CLIENT_SECRETS_FILE))

    # This OAuth 2.0 access scope allows for full read/write access to the
    # authenticated user's account.
    YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
        message=MISSING_CLIENT_SECRETS_MESSAGE,
        scope=YOUTUBE_READ_WRITE_SCOPE)

    storage = Storage("%s-oauth2.json" % sys.argv[0])
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        flags = argparser.parse_args()
        credentials = run_flow(flow, storage, flags)

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
        http=credentials.authorize(httplib2.Http()))

    # This code creates a new, private playlist in the authorized user's channel.
    playlists_insert_response = youtube.playlists().insert(
        part="snippet,status",
        body=dict(
            snippet=dict(
                title="Test Playlist",
                description="A private playlist created with the YouTube API v3"
            ),
            status=dict(
                privacyStatus="private"
            )
        )
    ).execute()

    print "New playlist id: %s" % playlists_insert_response["id"]
    playlist_id = playlists_insert_response['id']
    return playlist_id













