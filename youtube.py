from model import db, Artist, Song, Playlist, SongPlaylist, YouTubeVideo
from pprint import pprint
from sqlalchemy import exists
# from server import *

import requests
import os


def queries_video_db(artist_and_song):
    """Queries the YoutubeVideo table to see if searched song exists as a video"""

    searched_artist = artist_and_song[0]
    searched_song = artist_and_song[1]

################ Querying syntax
    # db.session.query(YouTubeVideo).


def yt_api_call(artist_and_song):
    """Gets JSON from youtube api"""

    yt_key = os.environ['YOUTUBE_SERVER_KEY']

    search = str(artist_and_song[0] + " " + artist_and_song[1])

    print "youtube yt_api_call ", search

    yt_payload = {'key': yt_key, 'q': search}

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

    # prints for debugging
    print video_id 
    
    print video_title

    parsed_search_results = {'video_id': video_id, 'video_title': video_title}
    print parsed_search_results

    return parsed_search_results
    # returns a python dictionary for flexibility. Can be jsonified, jinjaed,
    # or used as is

def adds_yt_video_info_to_db(parsed_search_results, artist_and_song, artist_id):
    """Adds video to youtube_videos table"""

    print "yt adds_yt_video_info_to_db"
    print "yt adds_yt_video_info_to_db artist_id ", artist_id

    searched_artist = artist_and_song[0]
    searched_song = artist_and_song[1]

    yt_video_id = parsed_search_results['video_id']
    video_title = parsed_search_results['video_title']

    print "Youtube.py yt_video_id ", yt_video_id
    print "Youtube.py video_title ", video_title

    does_video_exist = db.session.query(exists().where(YouTubeVideo.yt_video_id == yt_video_id)).scalar()

    if does_video_exist:
        print "Video in db"
    else:
        print "Video doesn't exist. Ading to db"
        video_info = YouTubeVideo(yt_video_id=yt_video_id,
                                  video_title=video_title,
                                  searched_artist=searched_artist,
                                  searched_song=searched_song,
                                  artist_id=artist_id)

        db.session.add(video_info)
        db.session.flush()
        print "youtube, adds_yt_song_results_to_db, Video and artist_id successfully flushed to database."





