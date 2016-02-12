"""Ada Audio"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from pprint import pprint
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Artist, Song, Playlist, SongPlaylist
from api_helper import *
from flask_sqlalchemy import SQLAlchemy

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

    # From request library
    payload = {'title': song, 'artist': artist}

    r = requests.get("http://developer.echonest.com/api/v4/song/search?api_key=U1KN7HSV9GGNANZJ2&format=json&results=1&", params=payload)
    
    # Debugging print statement
    print (r.url)

    # binds dictionary from get request to variable
    dict_from_en_api = r.json()

    # Debugging print statement
    pprint(dict_from_en_api)

    # fn from api_helper.py - artist_id, artist, song_id, song
    parsed_search_results = parses_en_json_results(dict_from_en_api)

    import pdb; pdb.set_trace()

    while db.session.execute(QUERY, {en_artist_id: parsed_search_results[0]}).one() != parsed_search_results[0]:
        Artist.query.insert(en_artist_id=parsed_search_results[0], 
                            artist_name=parsed_search_results[1])


    """ takes the artist_id and queries artist table, if artist_id
    doesn't exist, add artist info to table. 
      also takes the song_id and and queries song table, if song_id
    doesn't exist, add song info to table.
    """

    return render_template('playlist.html')




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
