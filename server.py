"""Ada Audio"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session, jsonify

from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Artist, Song, Playlist, SongPlaylist, YouTubeVideo
from flask_sqlalchemy import SQLAlchemy
from api_helper import *
from seed import *
from youtube import *

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

@app.route('/search_playlistafy')
def gets_user_serach_results():
    """Converts search into EchoNest GET request and inserts JSON object
    into database"""

   

    artist = request.args['artist']
    song = request.args['song']

    # Converts search into titles
    artist_str = str(artist.title())
    song_str = str(song.title())
    # Need to make sure that str are in correct format for querying

    artist_and_song = [artist_str, song_str]

    print "server.py User search artist and song list ", artist_and_song

    # checks user search for uniqueness and adds to db. 
    # in api_helper.py
    returns_artist_id = adds_unique_searches_to_database(artist_and_song)

    # from yourube.py file
    dict_from_yt_api = yt_api_call(artist_and_song)
    parsed_search_results = parses_yt_results(dict_from_yt_api)
    
    print "Server, parsed search_results ", parsed_search_results
    
    # need to check if search already exists
    adds_to_db = adds_yt_video_info_to_db(parsed_search_results,
                                          artist_and_song, 
                                          returns_artist_id)
    
    db.session.commit()

    # yt videoId in a dict to be passed to js playlist page
    data = json.dumps(parsed_search_results)

    return render_template('playlist.html',
                            data=data)
    

######################################

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)
    '''Do I need to connect to db?'''

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
