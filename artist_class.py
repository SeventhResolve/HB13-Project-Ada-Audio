from pprint import pprint
from youtube import yt_api_call
from pyechonest import *

import requests
import os
import json


class Artist(object):

    def __init__(self, artist):
        print "ARTIST is", artist
        self.artist = artist

    def creates_artist_en_playlist(self):
        "Gets a playlist JSON based on artist"

        en_key = os.environ['ECHO_NEST_API_KEY']

        print "artist_class, artist ", self.artist

        r = requests.get("http://developer.echonest.com/api/v4/playlist/static?api_key=%s&artist=%s&format=json&results=7&type=artist-radio" % (en_key, self.artist))
       
        # Debugging print statement
        print (r.url)

        # binds dictionary from get request to variable
        artist_playlist = r.json()

        # Debugging print statement
        pprint(artist_playlist)

        return artist_playlist


    def extracts_artist_and_song(self, artist_playlist):
        """Extracts artist and song from artist_playlist to query youtube api"""
        num_songs = len(artist_playlist['response']['songs'])
        count = 0
        yt_search_playlist =[]
        while count < num_songs:

            artist_name = artist_playlist['response']['songs'][count]['artist_name']
            
            song_title = artist_playlist['response']['songs'][count]['title']

            yt_search_playlist.append({'artist': artist_name, 'song': song_title})

            count += 1

        return yt_search_playlist

    def creates_yt_playlist(self, yt_search_playlist):

        yt_video_playlist = []
        for song in yt_search_playlist:
            artist_and_song = [song['artist'], song['song']]
            yt_video = yt_api_call(artist_and_song)

            yt_video_playlist.append(yt_video)

        yt_video_playlist = {"playlist": yt_video_playlist}

        # in {'playlist': [{yt dict}, {yt dict}, {yt dict}]} form

        print yt_video_playlist
        return yt_video_playlist


if __name__ == '__main__':
    print "ARTIST CLASS :D"







