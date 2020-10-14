import requests
import json
import time
from datetime import date, datetime
import base64

import mysql.connector

def get_access_token(id_secret_file):
    with open(id_secret_file) as f:
        data = json.load(f)
        d = {
            "client_id": data["client_id"],
            "client_secret": data["client_secret"]
        }

    auth = ":".join([d.get("client_id"), d.get("client_secret")])
    auth_bytes = auth.encode('ascii')
    base64_bytes = base64.b64encode(auth_bytes)
    base64_auth = base64_bytes.decode('ascii')
    
    url = 'https://accounts.spotify.com/api/token'
    body = {
        'grant_type': 'client_credentials'
    }

    headers = {
        'Authorization': ' '.join(['Basic', base64_auth])
    }

    r = requests.post(url, data = body, headers=headers)
    print(r.text)
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
    params = [
        ('market', 'SE'),
    ]

    r = requests.get(url, headers=headers, params=params)
    r_dict = json.loads(r.text)
    track_info = {
        "id": r_dict.get("id"),
        "name": r_dict.get("name"),
        "uri": r_dict.get("uri"),
        "duration_ms": r_dict.get("duration_ms"),
        "release_date": r_dict.get("album").get("release_date"),
        "fetch_date": date.today().strftime("%Y-%m-%d"),
        "popularity": r_dict.get("popularity"),
    }

    return track_info


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

    print("Creating table OK")


def save_tracks(connection, track_info):
    cursor = connection.cursor()

    try:
        cursor.execute("""
INSERT INTO tracks (id, name, uri, duration, release_date) VALUES (%s, %s, %s, %s, %s)
""", (track_info["id"], track_info["name"], track_info["uri"], track_info["duration_ms"], track_info["release_date"])
                       )
        connection.commit()
    except mysql.connector.Error as err:
        print(err.msg)
    
    print("Insert into tracks")

def save_track_popularity(connection, track_info):
    cursor = connection.cursor()
    try:
        cursor.execute("""
INSERT INTO track_popularity (fetch_date, track_id, popularity) VALUES (%s, %s, %s)
""", (track_info["fetch_date"], track_info["id"], track_info["popularity"])
        )
        connection.commit()
    except mysql.connector.Error as err:
        print(err.msg)

    print("Insert into track_popularity")    

def db_setup(connection):
    tracks_table_description = """
    CREATE TABLE if not exists tracks (id VARCHAR(32)  PRIMARY KEY, name VARCHAR(255), uri VARCHAR(255), duration INT, release_date DATE)
"""
    track_popularity_table_description = """
    CREATE TABLE if not exists track_popularity (fetch_date DATE, track_id VARCHAR(32), popularity INT, PRIMARY KEY(fetch_date, track_id)) 
"""
    create_table(connection, 'test', tracks_table_description)
    create_table(connection, 'test', track_popularity_table_description)

def fetch_and_save(access_token, connection, track_ids_file):
    with open(track_ids_file, 'r') as f:
        for line in f:
            track_info = get_track(access_token, line.strip('\n'))
            save_tracks(connection, track_info)
            save_track_popularity(connection, track_info)
            
    
if __name__ == '__main__':
    connection = db_connection_cursor()
    db_setup(connection)    
    fetch_and_save(get_access_token("id_secret.json"), connection, "track_ids.txt")
