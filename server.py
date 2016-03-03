"""Ada Audio"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Artist, Song, Playlist, SongPlaylist, YouTubeVideo
from flask_sqlalchemy import SQLAlchemy
from playlist_helper import *
from api_helper import *
from seed import *
from youtube import *
from genre_class import Genre

import json

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Prevents jinja from failing silently
app.jinja_env.undefined = StrictUndefined


            

@app.route('/')
def index():
    """Homepage"""

    return render_template('homesearchpage.html')

@app.route('/playlist')
def gets_user_serach_results():
    """Converts search into EchoNest GET request and inserts JSON object
    into database"""

   

    artist = request.args['artist']
    song = request.args['song']
    genre = request.args['genre']
    # tempo = request.args['tempo']

    if artist and song:


        # Converts search into titles
        artist_str = str(artist.title())
        song_str = str(song.title())
        # Need to make sure that str are in correct format for querying

        artist_and_song = [artist_str, song_str]

        print "server.py User search artist and song list ", artist_and_song

        # checks user search for uniqueness and adds to db. 
        # in api_helper.py
        returns_artist_id = adds_unique_searches_to_database(artist_and_song)


        yt_playlist_query = creates_yt_playlist_query(artist_and_song)
        # from api_helper.py, made by echonest
        print "1111111111111111"
        new_artists_added = adds_new_artists_to_db_by_en_id(yt_playlist_query)
        # from seed.py
        print "2222222222222222"
        new_songs_added = adds_new_songs_to_db_by_en_id(yt_playlist_query)
        # from seed.py
        print "333333333333333"
        yt_frontend_playlist = creates_yt_frontend_playlist(yt_playlist_query)
        # from youtube.py
        print "444444444444444"
        yt_db_playlist = creates_yt_db_playlist(yt_frontend_playlist, yt_playlist_query)
        print "555555555555555"
        added_yt_playlist_info = adds_yt_video_info_to_db(yt_db_playlist)
        # from seed.py
        print "66666666666666"

    if genre:
        genre = Genre(str(genre))
        print genre
        genre_playlist = genre.creates_genre_en_playlist()
        yt_search_playlist = genre.extracts_artist_and_song(genre_playlist)
        yt_frontend_playlist = genre.creates_yt_playlist(yt_search_playlist)

    # if tempo:
        # ******** do tempo playlisting stuff here
        

    yt_playlist_id = create_yt_playlist_id()
    # creates an empty playlist on youtube account
    print "#################### ", yt_playlist_id

    db.session.commit()



    # yt videoId in a dict to be passed to js playlist page
    data = json.dumps(yt_frontend_playlist)

    

    # adds_video_to_session()
    # print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!"





    return render_template('playlist.html',
                            data=data,
                            jinja_data=yt_frontend_playlist)
    

######################################

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
