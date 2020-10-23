import requests
import json
import time
from datetime import date
import base64

import mysql.connector


def get_access_token(id_secret_file):
    with open(id_secret_file) as f:
        d = json.load(f)

    auth = ":".join([d.get("client_id"), d.get("client_secret")])
    auth_bytes = auth.encode("ascii")
    base64_bytes = base64.b64encode(auth_bytes)
    base64_auth = base64_bytes.decode("ascii")

    url = "https://accounts.spotify.com/api/token"
    body = {"grant_type": "client_credentials"}

    headers = {"Authorization": "Basic " + base64_auth}

    r = requests.post(url, data=body, headers=headers)
    if r.status_code == 200:
        print("Requesting access token Okey.")
        response_dict = json.loads(r.text)
        access_token = response_dict.get("access_token")
        return access_token
    else:
        print("Requesting access token failed with status code: " + str(r.status_code))
        print("Please double check that your Spotify Client ID and Client Secret is filled in id_secret.json configuration file.")
        return ""


def get_track(access_token, track_id):
    url = "https://api.spotify.com/v1/tracks/{id}".format(id=track_id)
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token,
    }
    params = [
        ("market", "SE"),
    ]

    r = requests.get(url, headers=headers, params=params)
    if r.status_code == 200:
        print("Requesting track info Okey.")
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
    else:
        print("Requesting track info failed with status code: " + str(r.status_code))
        return {}
    
def db_connection_cursor():
    config = {
        "user": "user",
        "password": "123",
        "host": "db",
        "database": "test",
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
        cursor.execute(
            """INSERT INTO tracks
            (id, name, uri, duration, release_date)
            VALUES (%s, %s, %s, %s, %s)""",
            (
                track_info["id"],
                track_info["name"],
                track_info["uri"],
                track_info["duration_ms"],
                track_info["release_date"],
            ),
        )
        connection.commit()
    except mysql.connector.Error as err:
        print(err.msg)

    print("Insert into tracks")


def save_track_popularity(connection, track_info):
    cursor = connection.cursor()
    try:
        cursor.execute(
            """INSERT INTO track_popularity
            (fetch_date, track_id, popularity)
            VALUES (%s, %s, %s)""",
            (track_info["fetch_date"], track_info["id"], track_info["popularity"]),
        )
        connection.commit()
    except mysql.connector.Error as err:
        print(err.msg)

    print("Insert into track_popularity")


def db_setup(connection):
    tracks_table_description = """
    CREATE TABLE if not exists tracks (
        id VARCHAR(32) PRIMARY KEY,
        name VARCHAR(255),
        uri VARCHAR(255),
        duration INT,
        release_date DATE
    )
    """
    track_popularity_table_description = """
    CREATE TABLE if not exists track_popularity (
        fetch_date DATE,
        track_id VARCHAR(32),
        popularity INT,
        PRIMARY KEY(fetch_date, track_id)
    )
    """
    create_table(connection, "test", tracks_table_description)
    create_table(connection, "test", track_popularity_table_description)


def fetch_and_save(access_token, connection, track_ids_file):
    with open(track_ids_file, "r") as f:
        for line in f:
            track_info = get_track(access_token, line.strip("\n"))
            if track_info != {}:
                save_tracks(connection, track_info)
                save_track_popularity(connection, track_info)
            else:
                print("Track " + line.strip("\n") + "has no valid info to save.") 
                continue


if __name__ == "__main__":
    connection = db_connection_cursor()
    db_setup(connection)

    access_token = get_access_token("id_secret.json")
    if access_token != "":
        fetch_and_save(access_token, connection, "track_ids.txt")
