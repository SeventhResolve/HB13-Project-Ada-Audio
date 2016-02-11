

def convert_json_to_items(dict_from_en_api):
# change name

    ''' *** From a song/artist search ***
    1. takes the json dictionary from turns_search_into_en_dict from server.py
    parses through the dictionary
    2. pulls out artist_id, artist, song, and song_id.
    3. adds each item to the add_to_database
    '''

    artist_id = dict_from_en_api['response']['songs'][0]['artist_id']
    artist_name = dict_from_en_api['response']['songs'][0]['artist_name']
    song_id = dict_from_en_api['response']['songs'][0]['id']
    song_title = dict_from_en_api['response']['songs'][0]['title']

    print artist_id
    print artist_name
    print song_id
    print song_title

def add_search_to_database():
    ''' passes in a dictionary to the add_to_database function from 
        api_helper.api so add search to db
    '''    
    pass
    