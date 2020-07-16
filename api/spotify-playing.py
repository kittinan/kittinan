from flask import Flask, Response, jsonify
from base64 import b64encode

import requests
import json
import os


SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_SECRET_ID = os.getenv("SPOTIFY_SECRET_ID")
SPOTIFY_REFRESH_TOKN = os.getenv("SPOTIFY_REFRESH_TOKN")

SPOTIFY_URL_REFRESH_TOKEN = "https://accounts.spotify.com/api/token"
SPOTIFY_URL_NOW_PLAYING = "https://api.spotify.com/v1/me/player/currently-playing"

app = Flask(__name__)


def get_authorization():

    return b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_SECRET_ID}".encode()).decode("ascii")


def refresh_token():

    data = {
        "grant_type": "refresh_token",
        "refresh_token": SPOTIFY_REFRESH_TOKN,
    }

    headers = {"Authorization": "Basic {}".format(get_authorization())}

    response = requests.post(SPOTIFY_URL_REFRESH_TOKEN, data=data, headers=headers)
    repsonse_json = response.json()

    return repsonse_json["access_token"]


def get_now_playing():

    token = refresh_token()

    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(SPOTIFY_URL_NOW_PLAYING, headers=headers)

    if response.status_code == 204:
        return {}

    repsonse_json = response.json()
    return repsonse_json


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):

    r = get_now_playing()

    return jsonify(r)


if __name__ == "__main__":
    app.run(debug=True)
