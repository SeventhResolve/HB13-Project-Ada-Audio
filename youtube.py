from model import db, Artist, Song, Playlist, SongPlaylist, YouTubeVideo
from pprint import pprint
from sqlalchemy import exists
# from server import *

import requests
import os


def yt_api_call(artist_and_song):
    """Gets JSON from youtube api"""

    yt_key = os.environ['YOUTUBE_SERVER_KEY']

    artist = artist_and_song[0]
    song = artist_and_song[1]

    search = "%s %s"% (artist, song)

    print "youtube yt_api_call ", search

    yt_payload = {'key': yt_key, 'q': search, 'type': 'video'}

    r = requests.get("https://www.googleapis.com/youtube/v3/search?part=snippet", params=yt_payload)

    # Debugging print statement
    print (r.url)

    # binds dictionary from get request to variable
    dict_from_yt_api = r.json()

    # Debugging print statement
    # pprint(dict_from_yt_api)

    print "ran gets_json_from_yt_api"

    return dict_from_yt_api

def parses_yt_results(dict_from_yt_api):
    """Parses youtube dictionary results for videoId and video title"""

    video_id = dict_from_yt_api['items'][0]['id']['videoId']
    video_title = dict_from_yt_api['items'][0]['snippet']['title']
    video_thumbnail = dict_from_yt_api['items'][0]['snippet']['thumbnails']['default']['url']

    # prints for debugging
    print video_id 
    
    print video_title

    parsed_search_results = {'video_id': video_id, 
                             'video_title': video_title, 
                             'video_thumbnail': video_thumbnail}
    print parsed_search_results

    return parsed_search_results
    # returns a python dictionary for flexibility. Can be jsonified, jinjaed,
    # or used as is



def creates_yt_video_playlist(yt_playlist_query):
    """Takes en playlist and calls yt api for music videos, returns 
    playlist of video ids to pass as JSON"""

    # song_object = Song.query.filter(Song.en_song_id == en_song_id).one()
    # artist_id = song_object.artist_id
    # en_artist_id = db.session.query(Artist.en_artist_id).filter(Artist.artist_id == artist_id).one()            
    # artist_name = db.session.query(Artist.artist_name).filter(Artist.artist_id == artist_id).one()            
    # song_title = db.session.query(Song.song_title).filter(Song.en_song_id == en_song_id).one()


                        # {'artist_name': artist_name,
                        #  'en_artist_id': en_artist_id,
                        #  'song_title': song_title,
                        #  'en_song_id': en_song_id}

    contains_yt_playlist_info = []

    for item in yt_playlist_query:

        artist_name = item['artist_name']
        song_title = item['song_title']
        en_song_id = item['en_song_id']
        en_artist_id = item['en_artist_id']
        artist_and_song = [artist_name, song_title]

        artist_id = db.session.query(Artist.artist_id).filter(Artist.en_artist_id == en_artist_id).one()

        dict_from_yt_api = yt_api_call(artist_and_song)
        parsed_search_results = parses_yt_results(dict_from_yt_api)
        # returns dictionary of youtube videos

        video_id = parsed_search_results['video_id']
        video_title = parsed_search_results['video_title']
        video_thumbnail = parsed_search_results['video_thumbnail']

        yt_info_for_each_song = {'yt_video_id': video_id,
                                 'video_title': video_title,
                                 'video_thumbnail': video_thumbnail,
                                 'searched_artist': artist_name,
                                 'searched_song': song_title,
                                 'artist_id': artist_id}
        contains_yt_playlist_info.append(yt_info_for_each_song)

    print "YOUTUBE.PY, creates_yt_video_playlist, ", contains_yt_playlist_info
    return contains_yt_playlist_info

        # for youtube table need: video title, video id, searched artist
        # searched song, and artist id

        # ******v doesn't make sense. turn into a dictionary with yt video ids
        # for each_artist_name_and_artist_id in contains_artist_name_and_artist_id:
        #     artist_name = each_artist_name_and_artist_id[0]
        #     if artist_name == each_artist_and_song[0]:
        #         artist_id = each_artist_name_and_artist_id[1]
        #         video_id = parsed_search_results['video_id']
        #         contains_video_ids.append(video_id)
        #         adds_yt_video_info_to_db(parsed_search_results, each_artist_and_song, artist_id)

    # print "api_helper, gets_yt_info_from_yt_api_for_playlist, contains_video_ids ", contains_video_ids
    # return contains_video_ids



def makes_playlist_of_yt_video_ids(contains_yt_playlist_info):
    """Queries Youtube Video db and creates a playlist with video ids"""
    # Parameter in list form

    return contains_yt_playlist_info


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





