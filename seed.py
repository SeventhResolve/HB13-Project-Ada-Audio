from model import db, Artist, Song, Playlist, SongPlaylist


def adds_en_json_results_to_db(parsed_search_results):
    ''' Seeds the database with results from parses_en_json_results'''

    
    # THIS WORKS but I want to check for duplicates
    artist_info = Artist(en_artist_id=parsed_search_results[0],
                         artist_name=parsed_search_results[1])
    '''
    Scratch code:

    checks_duplicate_artist = Artist.query.filter(
        Artist.en_artist_id=parsed_search_results[0]).one()

    ??? What will this return if there isn't an artist in the db?

    if checks_duplicate_artist:
        return
    else:
        db.session.add(artist_info)
        db.session.commit()

    '''
    db.session.add(artist_info)
    db.session.commit()


    # This needs foreign keys added into the db which doesn't work...
    song_info = Song(en_song_id=parsed_search_results[2],
                     song_title=parsed_search_results[3],
                     artist_id=artist_info.artist_id)

    db.session.add(song_info)
    db.session.commit()
