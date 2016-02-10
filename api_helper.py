

def add_to_database(dict_from_en_api):


    ''' *** From a song/artist search ***
    1. takes the json dictionary from turns_search_into_en_dict from server.py
    parses through the dictionary
    2. pulls out artist_id, artist, song, and song_id.
    3. adds each item to the add_to_database
    '''

    artist_id = dict_from_en_api['response']['songs'][0]['artist_id']
    artist_name = dict_from_en_api['response']['songs'][1]['artist_name']
    song_id = dict_from_en_api['response']['songs'][2]['id']
    song_title = dict_from_en_api['response']['songs'][3]['title']

