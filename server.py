"""Ada Audio"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
from pprint import pprint
import requests
import json


app = Flask(__name__)

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

turn_into_url('beatles', 'hey jude')