from model import db, Artist, Song, Playlist, SongPlaylist, YouTubeVideo
from pprint import pprint
from sqlalchemy import exists

import requests
import os

import httplib2
import sys
import json

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow



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
    pprint(dict_from_yt_api)

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


def creates_yt_frontend_playlist(yt_playlist_query):
    """Takes en playlist and calls yt api for music videos, adds returned JSON
    into a playlist. For use on front-end"""

    yt_playlist = []

    for item in yt_playlist_query:

        artist_name = item['artist_name']
        song_title = item['song_title']
        artist_and_song = [artist_name, song_title]

        dict_from_yt_api = yt_api_call(artist_and_song)
        yt_playlist.append(dict_from_yt_api)

    yt_frontend_playlist = {'playlist': yt_playlist}


    print "*** youtube.py, creates_yt_frontend_playlist, ", yt_frontend_playlist
    return yt_frontend_playlist


def creates_yt_db_playlist(yt_frontend_playlist, yt_playlist_query):
    """Takes JSON playlist and echonest song info and reformats 
    it for addition into db"""

    contains_yt_playlist_info = []
    count = 0

    for item in yt_playlist_query:

        artist_name = item['artist_name']
        song_title = item['song_title']
        en_artist_id = item['en_artist_id']

        artist_id = db.session.query(Artist.artist_id).filter(Artist.en_artist_id == en_artist_id).one()

        print "$$$$$$$$$$$$$$$$$$ count", count

        yt_video_id = yt_frontend_playlist['playlist'][count]['items'][0]['id']['videoId']
        video_title = yt_frontend_playlist['playlist'][count]['items'][0]['snippet']['title']
        video_thumbnail = yt_frontend_playlist['playlist'][count]['items'][0]['snippet']['thumbnails']['default']['url']

        count += 1

        
        yt_info_for_each_song = {'yt_video_id': yt_video_id,
                                 'video_title': video_title,
                                 'video_thumbnail': video_thumbnail,
                                 'searched_artist': artist_name,
                                 'searched_song': song_title,
                                 'artist_id': artist_id}

        contains_yt_playlist_info.append(yt_info_for_each_song)

    return contains_yt_playlist_info


def create_yt_playlist_id():

    # *** THE FOLLOWING CODE IS PROVIDED BY THE YOUTUBE DATA API***
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






