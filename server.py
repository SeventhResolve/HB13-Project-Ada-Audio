"""Ada Audio"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from pprint import pprint
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Artist, Song, Playlist, SongPlaylist
from api_helper import *

import requests
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
    """Input artist and song titile then function will insert into an 
    echonest GET request and returns a dictionary"""
    
    artist = request.args['artist']
    song = request.args['song']

    payload = {'title': song, 'artist': artist}

    r = requests.get("http://developer.echonest.com/api/v4/song/search?api_key=U1KN7HSV9GGNANZJ2&format=json&results=1&", params=payload)
    
    # Debugging print statement
    print (r.url)

    # binds dictionary from get request to variable
    dict_from_en_api = r.json()

    pprint(dict_from_en_api)

    search_list = adds_search_to_database(dict_from_en_api)

    print search_list

    return redirect('/')
    # have this eventually render_template to /playlist

@app.route('/playlist')
def 


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
