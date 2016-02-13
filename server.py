"""Ada Audio"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from pprint import pprint
from flask_debugtoolbar import DebugToolbarExtension
# from model import connect_to_db, db, Artist, Song, Playlist, SongPlaylist
# ******* moved into seed.py
from api_helper import *
from flask_sqlalchemy import SQLAlchemy

import os
# import requests
# ******* move into seed.py
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
def turns_search_into_playlist():
    """Converts search into EchoNest GET request and inserts JSON object
    into database"""

    en_key = os.environ['ECHONEST_API_KEY']
    # yt_browser_key = os.environ['YOUTUBE_BROWSER_KEY']

    artist = request.args['artist']
    song = request.args['song']


    # From request library
    payload = {'title': song, 'artist': artist}

    r = requests.get("http://developer.echonest.com/api/v4/song/search?api_key=%(en_key)s&format=json&results=1&" % locals(), params=payload)
    
    # Debugging print statement
    print (r.url)

    # binds dictionary from get request to variable
    dict_from_en_api = r.json()

    # Debugging print statement
    pprint(dict_from_en_api)


    # ******** v moved into seed.py
    # parsed_search_results = parses_en_json_results(dict_from_en_api)

    # # THIS WORKS but I want to check for duplicates
    # artist_info = Artist(en_artist_id=parsed_search_results[0],
    #                      artist_name=parsed_search_results[1])
    
    # db.session.add(artist_info)
    # db.session.commit()


    # # This needs foreign keys added into the db which doesn't work...
    # song_info = Song(en_song_id=parsed_search_results[2],
    #                  song_title=parsed_search_results[3],
    #                  artist_id=artist_info.artist_id)

    # db.session.add(song_info)
    # db.session.commit()


    return render_template('playlist.html')




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    # connect_to_db(app)
    '''Do I need to connect to db?'''

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
