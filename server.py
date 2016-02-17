"""Ada Audio"""

from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session

from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, Artist, Song, Playlist, SongPlaylist
from flask_sqlalchemy import SQLAlchemy
from api_helper import *
from seed import *

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

    # fn in api_helper.py
    query_results = queries_song_db(artist_and_song)
    
    if query_results == "In db":
        print "Song is in db"
        # then direct to play video fn
    elif query_results == "Add to db":
        adds_to_db = populate_database(artist_and_song)
        print "server gets_user_serach_results database populated"

    # artist_query = queries_artist_db(artist_and_song)




    return render_template('playlist.html')
    #



# Need to be able to query database to see if en_song_id/en_artist_id,
# yt_artist_id/yt_artist_id exists. If it exists, get the ids. If not
# add to db



    # # From request library, adds search to db
    # payload = {'title': song, 'artist': artist}

    # r = requests.get("http://developer.echonest.com/api/v4/song/search?api_key=%(en_key)s&format=json&results=1&" % locals(), params=payload)
    
    # # Debugging print statement
    # print (r.url)

    # # binds dictionary from get request to variable
    # dict_from_en_api = r.json()

    # # Debugging print statement
    # pprint(dict_from_en_api)

    # parsed_search_results = parses_en_json_results(dict_from_en_api)

    # added_to_db = adds_en_json_results_to_db(parsed_search_results)
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


def renders_yt_playlist():

    pass

    return render_template('playlist.html')




if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)
    '''Do I need to connect to db?'''

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
