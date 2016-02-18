"""Models and database functions for Ada Audio."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# from sqlalchemy import *
# from sqlalchemy.orm import *

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)



db = SQLAlchemy()



##############################################################################
# Model definitions

class Artist(db.Model):
    """Musical artist items"""

    __tablename__ = "artists"

    artist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    artist_name = db.Column(db.String(100), nullable=False)
    en_artist_id = db.Column(db.String(100), nullable=False, unique=True)
    
 
    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<Artist artist_id=%s artist_name=%s en_artist_id=%s>" % (self.artist_id, 
                                                                         self.artist_name,
                                                                         self.en_artist_id)



class Song(db.Model):
    """Song title and attributes"""

    __tablename__ = "songs"

    song_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    song_title = db.Column(db.String(100), nullable=False)
    en_song_id = db.Column(db.String(100), nullable=False, unique=True)
    
    # artist_id = foreign key from artists table
    artist_id = db.Column(db.Integer, 
                          db.ForeignKey("artists.artist_id"))

    # genre
    # pick a couple other attributes

   
    artist = db.relationship('Artist', 
                            backref=db.backref('songs', 
                            order_by=song_id))

    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<Song song_id=%s song_title=%s en_song_id=%s>" % (self.song_id, 
                                                                   self.song_title,
                                                                   self.en_song_id)


class Playlist(db.Model):
    """Playlist and attributes"""

    __tablename__ = "playlists"

    playlist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    playlist_name = db.Column(db.String(100), nullable=False)


    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<Playlist playlist_id=%s playlist_name=%s>" % (self.playlist_id,
                                                               self.playlist_name)


class SongPlaylist(db.Model):
    """Song/Playlist association table"""

    __tablename__ = "song_playlists"

    sp_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    song_id = db.Column(db.Integer,
                        db.ForeignKey('songs.song_id'))
    playlist_id = db.Column(db.Integer,
                            db.ForeignKey('playlists.playlist_id'))

    song = db.relationship('Song',
                            # secondary='song_playlists', 
                            backref=db.backref('song_playlists', 
                            order_by=sp_id))

    playlist = db.relationship('Playlist',
                            # secondary='song_playlists', 
                            backref=db.backref('song_playlists', 
                            order_by=sp_id))

    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<SongPlaylist sp_id=%s song_id%s playlist_id%s>" % (self.sp_id, self.song_id, self.playlist_id)

class YouTubeVideo(db.Model):
    """YouTube videos and attributes"""
    # only adds artists that are in the EN db. Will make playlisting
    # easier later

###########################
# Is it possible for two foreign keys to point to the same field?

    __tablename__ = 'youtube_videos'

    video_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    yt_video_id = db.Column(db.String(100), nullable=False, unique=True)
    video_title = db.Column(db.String(100), nullable=False, unique=True)
    video_key = db.Column(db.Integer, 
                          db.ForeignKey("artists.artist_id"))
    

    yt_video = db.relationship('Artist', 
                            backref=db.backref('youtube_videos', 
                            order_by=video_key))

    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<YouTubeVideo video_key=#s yt_video_id=%s video_title=%s>" % (self.video_key, self.yt_video_id, self.video_title)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///music'
    db.app = app
    db.init_app(app)

    db.create_all()


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."


