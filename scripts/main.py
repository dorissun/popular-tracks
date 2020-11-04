import concurrent.futures

from popular_tracks import db
from popular_tracks import api

import logging


def fetch_asynch_and_save(access_token, connection, track_ids_file):
    with open(track_ids_file, "r") as f:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            future_to_info = {
                executor.submit(api.get_track, access_token, line.strip("\n")): line
                for line in f
            }
            for future in concurrent.futures.as_completed(future_to_info):
                data = future.result()
                if data != {}:
                    db.save_tracks(connection, data)
                    db.save_track_popularity(connection, data)
                else:
                    logging.error("Track has no valid info to save.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    connection = db.db_connection_cursor()
    db.db_setup(connection)

    access_token = api.get_access_token("id_secret.json")
    if access_token != "":
        fetch_asynch_and_save(access_token, connection, "track_ids.txt")
