"""Models and database functions for Ada Audio."""

from flask_sqlalchemy import SQLAlchemy

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
    en_artist_id = db.Column(db.Integer, nullable=False)

    songs = db.relationship('Song', backref='artists')

    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<Artist artist_id=%s artist_name=%s>" % (self.artist_id, self.artist_name)



class Song(db.Model):
    """Song title and attributes"""

    __tablename__ = "songs"

    song_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    song_title = db.Column(db.String(100), nullable=False)
    en_song_id = db.Column(db.Integer, nullable=False)
    
    # artist_id = foreign key from artists table
    artist_id = db.Column(db.Integer, 
                        db.ForeignKey("artists.artist_id"), 
                        nullable=False)

    # genre
    # pick a couple other attributes

    playlists = db.relationship('Playlist',
                            secondary='song_playlist', 
                            backref='songplaylist')


    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<Song movie_id=%s song_title=%s>" % (self.song_id, self.song_title)


class Playlist(db.Model):
    """Playlist"""

    __tablename__ = "playlists"

    playlist_id = db.Column(db.Integer, autoincrement=True, primary_key=True)


    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<Playlist playlist_id=%s artist_id=%s song_id=%s>" % (self.playlist_id, self.arist_id, self.song_id)


class SongPlaylist(db.Model):
    """M2M Playlist"""

    sp_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    song_id = db.Column(db.Integer,
                        db.ForeignKey('songs.song_id'),
                        nullable=False)
    playlist_id = db.Column(db.Integer,
                            db.ForeignKey('playlists.playlist_id'),
                            nullable=False)



    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<SongPlaylist sp_id=%s song_id%s playlist_id%s>" % (self.sp_id, self.song_id, self.playlist_id)

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///music'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."


