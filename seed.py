from model import connect_to_db, db, Artist, Song, Playlist, SongPlaylist
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from api_helper import *

import requests
import json


db = SQLAlchemy()

def adds_json_results_to_db():
    ''' Seeds the database with results from parses_en_json_results'''

    parsed_search_results = parses_en_json_results(dict_from_en_api)

    # THIS WORKS but I want to check for duplicates
    artist_info = Artist(en_artist_id=parsed_search_results[0],
                         artist_name=parsed_search_results[1])
    
    db.session.add(artist_info)
    db.session.commit()


    # This needs foreign keys added into the db which doesn't work...
    song_info = Song(en_song_id=parsed_search_results[2],
                     song_title=parsed_search_results[3],
                     artist_id=artist_info.artist_id)

    db.session.add(song_info)
    db.session.commit()

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///music'
    db.app = app
    db.init_app(app)

    # db.create_all()


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."

