import requests
import json
from datetime import date
import base64


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
        print(
            """
            Please double check that your Spotify Client ID and
            Client Secret is filled in id_secret.json configuration file.
            """
        )
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
