"""Ada Audio"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from pprint import pprint
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db

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

@app.route('/search_urlify')
def turn_into_url(artist, song):
    """Input artist and song titile then function will insert into an 
    echonest get requst"""

    payload = {'title': song, 'artist': artist}

    r = requests.get("http://developer.echonest.com/api/v4/song/search?api_key=U1KN7HSV9GGNANZJ2&format=json&results=1&", params=payload)
    
    # Debugging print statement
    print (r.url)

    # binds dictionary from get request to variable
    adict = r.json()

    pprint(adict)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()

turn_into_url('beatles', 'hey jude')