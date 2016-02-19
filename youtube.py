from model import db, Artist, Song, Playlist, SongPlaylist
from pprint import pprint
# from server import *

import requests
import os




def yt_api_call():
    """Gets JSON from youtube api"""

    artist_and_song = ['Taylor Swift', 'Blank Space']

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

def adds_yt_song_results_to_db(parsed_search_results, artist_id):
    """Adds video to youtube_videos table"""

    print "yt adds_yt_song_results_to_db entered"

    yt_search_results = parses_yt_results(parsed_search_results)

    video_info = YouTubeVideo(yt_video_id=yt_search_results['video_id'],
                              video_title=yt_search_results['video_title'],
                              artist_id=artist_id)
