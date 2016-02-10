"""Ada Audio"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from pprint import pprint
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db

import requests
import json
# import api_helper - doesn't work this way?

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Prevents jinja from failing silently
app.jinja_env.undefined = StrictUndefined




@app.route('/')
def index():
    """Homepage"""

    return render_template('homesearchpage.html')

@app.route('/search_urlify')
def turns_search_into_en_dict(artist, song):
    """Input artist and song titile then function will insert into an 
    echonest GET request and returns a dictionary"""

    artist = str(artist)
    song = str(song)

    payload = {'title': song, 'artist': artist}

    r = requests.get("http://developer.echonest.com/api/v4/song/search?api_key=U1KN7HSV9GGNANZJ2&format=json&results=1&", params=payload)
    
    # Debugging print statement
    print (r.url)

    # binds dictionary from get request to variable
    dict_from_en_api = r.json()

    pprint(dict_from_en_api)

    return dict_from_en_api

def add_search_to_database():
    ''' passes in a dictionary to the add_to_database function from 
        api_helper.api so add searchc to db
    '''    

# if __name__ == "__main__":
#     # We have to set debug=True here, since it has to be True at the point
#     # that we invoke the DebugToolbarExtension
#     app.debug = True

#     connect_to_db(app)

#     # Use the DebugToolbar
#     DebugToolbarExtension(app)

#     app.run()

turns_search_into_en_dict('beatles', 'hey jude')