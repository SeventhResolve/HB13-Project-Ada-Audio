from pprint import pprint
from youtube import yt_api_call

import requests
import os
import json


class Genre(object):

    def __init__(self, genre):
        print "Creates a statis genre playlist", genre
        self.genre = genre

    def creates_genre_en_playlist(self):
        "Gets a playlist JSON based on genre"

        en_key = os.environ['ECHO_NEST_API_KEY']

        print "seed, gets_genre_json_from_en_api ", self

        r = requests.get("http://developer.echonest.com/api/v4/playlist/static?api_key=%s&genre=%s&format=json&results=7&type=genre-radio" % (en_key, self))
       
        # Debugging print statement
        print (r.url)

        # binds dictionary from get request to variable
        genre_playlist = r.json()

        # Debugging print statement
        pprint(genre_playlist)

        return genre_playlist


    def extracts_artist_and_song(self, genre_playlist):
        """Extracts artist and song from genre_playlist to query youtube api"""
        num_songs = len(genre_playlist['response']['songs'])
        count = 0
        yt_search_playlist =[]
        while count < num_songs:

            artist_name = genre_playlist['response']['songs'][count]['artist_name']
            
            song_title = genre_playlist['response']['songs'][count]['title']

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
    print "Yay I made a GENRE class :D"







