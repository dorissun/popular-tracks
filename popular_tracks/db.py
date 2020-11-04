import time

import mysql.connector


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
