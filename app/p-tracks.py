import requests
import json
import time
from datetime import date

import mysql.connector

def get_auth():
    url = 'https://accounts.spotify.com/api/token'
    body = {
        'grant_type': 'client_credentials'
    }

    # TODO: base64 encode
    headers = {
        'Authorization':'Basic MGY3YzQ1M2YwNGM4NDEwYjk4ZTVhYWZmYjg3ZjRmMGQ6ZDk0NjhkMjZhMjZkNGJkNjk4ZjkxYjFiZDlmY2JhMTY='
    }

    r = requests.post(url, data = body, headers=headers)
    #print(r.text)
    response_dict = json.loads(r.text)
    access_token = response_dict.get('access_token')
    return access_token


def get_track(access_token, track_id):
    url = 'https://api.spotify.com/v1/tracks/{id}'.format(id=track_id)
    headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
        'Authorization': ' '.join(['Bearer', access_token])
    }
    params = (
        ('market', 'ES'),
    )

    r = requests.get(url, headers=headers, params=params)
    #print(r.text)
    r_dict = json.loads(r.text)
    track_infos = {
        "id": r_dict.get("id"),
        "name": r_dict.get("name"),
        "uri": r_dict.get("uri"),
        "duration_ms": r_dict.get("duration_ms"),
        "release_date": r_dict.get("album").get("release_date"),
        "fetch_date": date.today().strftime("%d/%m/%Y"),
        "popularity": r_dict.get("popularity"),
    }

    print(track_infos)
    return track_infos


def db_connection_cursor():
    config = {
        'user': 'user',
        'password': '123',
        'host': 'db',
        'database': 'test',
    }

    connection = None
    while not connection:
        try:
            connection = mysql.connector.connect(**config)
        except Exception:
            print("Could not connect. Sleep for a while.")
            time.sleep(1)
    
    return connection


def create_table(connection, DB_NAME, table_description):
    cursor = connection.cursor()

    try:
        cursor.execute(table_description)
    except mysql.connector.Error as err:
        print(err.msg)
    else:
        print("Creating table OK")


#def save_to_table(track):
    #INSERT INTO table1 (`Date`) VALUES (STR_TO_DATE('01/05/2010', '%m/%d/%Y'));
if __name__ == '__main__':
    
    access_token = get_auth()
    print(access_token)
    get_track(access_token, '11dFghVXANMlKmJXsNCbNl')


    connection = db_connection_cursor()

    tracks_table_description = """
    CREATE TABLE if not exists tracks (id VARCHAR(32)  PRIMARY KEY, name VARCHAR(255), uri VARCHAR(255), duration INT, release_date DATE)
"""
    # TODO: popularity column type
    track_popularity_table_description = """
    CREATE TABLE if not exists track_popularity (fetch_date DATE, track_id VARCHAR(32), popularity INT) 
"""
    create_table(connection, 'test', tracks_table_description)
    create_table(connection, 'test', track_popularity_table_description)
